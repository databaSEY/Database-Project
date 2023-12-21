
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from project.db import get_db
from flask import Flask, jsonify
from project.auth import login_required
bp = Blueprint('races', __name__)

from math import ceil

app = Flask(__name__)

RESULTS_PER_PAGE = 10
def get_distincts(db):
     # Retrieve distinct years and countries
    distinct_years_query = "SELECT DISTINCT year FROM races"
    distinct_years = [str(year[0]) for year in db.execute(distinct_years_query).fetchall()]

    distinct_countries_query = "SELECT DISTINCT country FROM circuits"
    distinct_countries = [country[0] for country in db.execute(distinct_countries_query).fetchall()]
    return distinct_years, distinct_countries

def get_search_results(search_term, year_filter, country_filter, page):
    offset = (page - 1) * RESULTS_PER_PAGE
    db = get_db()

    # Base query with search term
    if search_term:
        query = f"SELECT r.name, r.year, r.date, r.round, c.name, c.country, c.lat, c.lng, c.url, c.location, r.raceId , r.circuitId FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name LIKE '{search_term}%'"
        race_results_query = f"SELECT d.forename, d.surname, d.code, rs.position, rs.time, cn.name, r.raceId FROM races r JOIN circuits c ON r.circuitId = c.circuitId JOIN results rs ON r.raceId = rs.raceId JOIN drivers d ON rs.driverId = d.driverId JOIN constructors cn ON rs.constructorId = cn.constructorId WHERE r.name LIKE '{search_term}%' AND rs.position IN (1, 2, 3)"
        total_count_query = f"SELECT COUNT(*) FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name LIKE '{search_term}%'"
    else:
        query = f"SELECT r.name, r.year, r.date, r.round, c.name, c.country, c.lat, c.lng, c.url, c.location, r.raceId , r.circuitId  FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE LENGTH(r.name) > 0"
        race_results_query = f"SELECT d.forename, d.surname, d.code, rs.position, rs.time, cn.name, r.raceId FROM races r JOIN circuits c ON r.circuitId = c.circuitId JOIN results rs ON r.raceId = rs.raceId JOIN drivers d ON rs.driverId = d.driverId JOIN constructors cn ON rs.constructorId = cn.constructorId WHERE rs.position IN (1, 2, 3)"
        total_count_query = f"SELECT COUNT(*) FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE LENGTH(r.name) > 0"

    if year_filter:
        query += f" AND r.year = {year_filter}"
        race_results_query += f" AND r.year = {year_filter}"
        total_count_query += f" AND r.year = {year_filter}"

    if country_filter:
        query += f" AND c.country = '{country_filter}'"
        race_results_query += f" AND c.country = '{country_filter}'"
        total_count_query += f" AND c.country = '{country_filter}'"
        
    query +=" ORDER BY r.raceId"
    query += f" LIMIT {RESULTS_PER_PAGE} OFFSET {offset}"
    
    race_results_query += " ORDER BY r.raceId, rs.position"
    race_results_query += f" LIMIT {RESULTS_PER_PAGE} OFFSET {offset}"

    
    results = db.execute(query).fetchall()
    race_results = db.execute(race_results_query).fetchall()
    #race_results = sorted(race_results, key=lambda x: (x[-1], x[3]))

    total_count = db.execute(total_count_query).fetchone()[0]
    total_pages = ceil(total_count / RESULTS_PER_PAGE)

    distinct_years, distinct_countries = get_distincts(db)

    db.close()

    return results, race_results, total_pages, distinct_years, distinct_countries

@bp.route('/races')
def index():
    search_term = request.args.get('search', default='', type=str)
    year_filter = request.args.get('year', default='', type=str)
    country_filter = request.args.get('country', default='', type=str)
    page = request.args.get('page', default=1, type=int)

    results, race_results, total_pages, distinct_years, distinct_countries = get_search_results(search_term, year_filter, country_filter, page)
    return render_template('races.html', search_term=search_term, results=results, race_results=race_results, page=page, total_pages=total_pages,
                           distinct_years=distinct_years, distinct_countries=distinct_countries,
                           selected_year=year_filter, selected_country=country_filter)

@bp.route('/races/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        c_name = request.form.get('c_name', default='None')
        c_location = request.form.get('c_location', default='None')
        c_country = request.form.get('c_country', default='None')
        c_lat = request.form.get('c_lat', default='0')
        c_lng = request.form.get('c_lng', default='0')

        r_name = request.form.get('r_name', default='None')
        r_year = request.form.get('r_year', default='0000')
        r_date = request.form.get('r_date', default='0000-00-00')
        r_round = request.form.get('r_round', default='0')

        error = None


        if error is not None:
            flash(error)
        else:
            db = get_db()
            last_circuit_id = db.execute("SELECT circuitId FROM circuits ORDER BY circuitId DESC LIMIT 1").fetchone()[0]

            db.execute(
                'INSERT INTO circuits (circuitId, name, location, lat, lng,alt,url,country,circuitRef)'
                ' VALUES (?,?, ?, ?, ?,?,?,?,?)',
                (last_circuit_id+1,c_name,c_location,c_lat,c_lng, 0,'-',c_country,'-')
            )
            db.execute(
                'INSERT INTO races (name, year, date, round, time, url, circuitId)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (r_name, r_year, r_date, r_round, 0, '-', last_circuit_id+1)
    )
            db.commit()
            return redirect(url_for('races.index'))

    return render_template('races/create.html')

@bp.route('/races/delete', methods=('GET', 'POST', 'DELETE'))
@login_required
def delete():
    if request.method == 'DELETE':
        try:
            data = request.json
            race_ids = data.get('race_ids',  [])
            db = get_db()
            delete_query = f"DELETE FROM races WHERE raceId in ("
            for race_id in race_ids:
                if race_id != race_ids[0]:
                    delete_query += ", "
                delete_query += f" {race_id}"
            delete_query += ")"
            print(delete_query)
            db.execute(delete_query, )
            db.commit()

            return jsonify({"message": "Driver deleted successfully"}), 200
        except ValueError:
            return jsonify({"error": "Invalid driver_id parameter"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    else:
        return jsonify({"error": "Method not allowed"}), 405
    

@bp.route('/races/update', methods=['POST'])
@login_required
def update():
    try:
        # Get the data from the JSON request body
        updated_data = request.json.get('data', [])
        print(updated_data)
        db = get_db()
        # Perform the update operation in your database
        for data_entry in updated_data:
            
            circuitId = data_entry.get('circuitId')
            c_name = data_entry.get('c_name')
            c_location = data_entry.get('c_location')
            c_country = data_entry.get('c_country')
            
            raceId = data_entry.get('raceId')
            r_name = data_entry.get('r_name')
            r_year = data_entry.get('r_year')
            r_date = data_entry.get('r_date')
            r_round = data_entry.get('r_round')
            
            query = ('UPDATE races SET name = ?, year = ?, date = ?, round = ? '
                     ' WHERE raceId = ?')
            db.execute(query, (r_name, r_year, r_date, r_round, raceId))

            query = ('UPDATE circuits SET name = ?, location = ?, country = ? '
                     ' WHERE circuitId = ?')
            db.execute(query, (c_name, c_location, c_country, circuitId))

            db.commit()
        # Return a response (you can customize the response based on your needs)
        return jsonify({'message': 'Update successful'}), 200

    except Exception as e:
        # Handle exceptions as needed
        print('Error updating backend:', e)
        return jsonify({'error': 'Internal Server Error'}), 500

