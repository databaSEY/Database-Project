from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from project.db import get_db
from flask import Flask, jsonify

bp = Blueprint('drivers', __name__)


def convert_to_dict(row):
    return dict(zip(row.keys(), row))

def get_search_results(search_term, drivers_per_page, offset, nationality_filter):
    # Calculate the offset to retrieve the appropriate range of drivers from the database

    db = get_db()
    total_drivers = db.execute('SELECT COUNT(*) FROM drivers WHERE forename LIKE ?', (f'{search_term}%',)).fetchone()[0]

    if not nationality_filter:
        nationality_filter = None
    if search_term:
        # If a search term is provided, filter the results based on the first name
        query = (
           'SELECT d.driverId, d.driverRef, d.forename, d.surname, d.nationality'
            ' FROM drivers d '
            ' WHERE d.forename LIKE ? AND (CASE WHEN ? IS NULL THEN 1=1 ELSE  nationality=? END)'
            ' ORDER BY d.driverId'
        )
        search_term_with_percent = f'{search_term}%'
        posts = db.execute(query, (search_term_with_percent, nationality_filter, nationality_filter)).fetchall()
    else:
        # If no search term, retrieve all drivers
        query = (
            'SELECT d.driverId, d.driverRef, d.forename, d.surname, d.nationality'
            ' FROM drivers d'
            ' WHERE (? IS NULL OR d.nationality = ?)'
            ' ORDER BY d.driverId'
        )
        posts = db.execute(query, (nationality_filter, nationality_filter )).fetchall()

        
    distinct_nationalities_query = 'SELECT DISTINCT nationality FROM drivers order by 1'
    distinct_nationalities_rows = db.execute(distinct_nationalities_query,() ).fetchall()
    distinct_nationalities = [row[0] for row in distinct_nationalities_rows]
    # print( + "sssssoooo")

    return posts, drivers_per_page, total_drivers, distinct_nationalities

@bp.route('/drivers', methods=['GET'])
def index():
    # Get the current page and drivers per page from the URL parameters
    page = request.args.get('page', default=1, type=int)
    drivers_per_page = request.args.get('drivers_per_page', default=10, type=int)
    search_term = request.args.get('search', '')
    nationality_filter = request.args.get('nationality', default=None)
    offset = (page - 1) * drivers_per_page
    

    posts, drivers_per_page, total_drivers, distinct_nationalities = get_search_results(search_term, drivers_per_page, offset, nationality_filter)
    total_pages = total_drivers // drivers_per_page


    return render_template('drivers/index.html', posts=posts,  
                                                total_pages = total_pages, 
                                                page=page,
                                                drivers_per_page=drivers_per_page,
                                                distinct_nationalities=distinct_nationalities,
                                                selected_nationality=nationality_filter)

@bp.route('/drivers/driver_details/<int:driver_id>/details')
def driver_details(driver_id):
    db = get_db()

    name_query = f"SELECT d.forename, d.surname FROM drivers d where d.driverId = {driver_id}"
    name = db.execute(name_query, ).fetchone()
    print(name)

    details_query = (
        f'select  d.forename, d.surname, r.year , r.name, ds.position, ds.points'
        ' from drivers d'
        ' join driver_standings ds on d.driverId = ds.driverId'
        ' join races r on ds.raceId = r.raceId'
        f' where d.driverId = {driver_id} '
        ' order by position '
        ' limit 10'
    )
    details = db.execute(details_query, ).fetchall()



    return render_template('drivers/details.html', name=name, details=details)

@bp.route('/drivers/create', methods=('GET', 'POST'))
#@login_required
def create():
    if request.method == 'POST':
        driverId = request.form['driverId']
        driverRef = request.form['driverRef']
        forename = request.form['forename']
        surname = request.form['surname']
        nationality = request.form['nationality']
        error = None

        if not driverId or not driverRef or not forename or not surname or not nationality:
            error = 'All fields are required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO drivers (driverId, driverRef, forename, surname, nationality)'
                ' VALUES (?, ?, ?, ?, ?)',
                (driverId, driverRef, forename, surname, nationality)
            )
            db.commit()
            return redirect(url_for('drivers.index'))

    return render_template('drivers/create.html')

@bp.route('/drivers/delete', methods=('GET', 'POST', 'DELETE'))
def delete():
    if request.method == 'DELETE':
        try:
            data = request.json
            driver_ids = data.get('driver_ids', [])
            db = get_db()
            delete_query = f"DELETE FROM drivers WHERE driverId in ("
            for driver_id in driver_ids:
                if driver_id != driver_ids[0]:
                    delete_query += ", "
                delete_query += f" {driver_id}"
            delete_query += ")"
            db.execute(delete_query, )
            db.commit()

            return jsonify({"message": "Driver deleted successfully"}), 200
        except ValueError:
            return jsonify({"error": "Invalid driver_id parameter"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    else:
        return jsonify({"error": "Method not allowed"}), 405

@bp.route('/drivers/update', methods=['POST'])
def update():
    print("Update func")
    try:
        # Get the data from the JSON request body
        updated_data = request.json.get('data', [])
        db = get_db()
        # Perform the update operation in your database
        for data_entry in updated_data:
            driver_id = data_entry.get('driverId')
            forename = data_entry.get('forename')
            surname = data_entry.get('surname')
            driverRef = data_entry.get('driverRef')
            nationality = data_entry.get('nationality')

            query = ('UPDATE drivers SET forename = ?, surname = ?, driverRef = ?, nationality = ? '
                     ' WHERE driverId = ?')
            db.execute(query, (forename, surname, driverRef, nationality, driver_id))
            db.commit()

            # Print or use the extracted values as needed
            print(f'Driver ID: {driver_id}, Forename: {forename}, Surname: {surname}')

        # Return a response (you can customize the response based on your needs)
        return jsonify({'message': 'Update successful'}), 200
    except Exception as e:
        # Handle exceptions as needed
        print('Error updating backend:', e)
        return jsonify({'error': 'Internal Server Error'}), 500

