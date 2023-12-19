
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from project.db import get_db
from flask import Flask, jsonify

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
        query = f"SELECT r.name, r.year, r.date, r.round, c.name, c.country, c.lat, c.lng, c.url, c.location, r.raceId FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name LIKE '{search_term}%'"
        race_results_query = f"SELECT d.forename, d.surname, d.code, rs.position, rs.time, cn.name, r.raceId FROM races r JOIN circuits c ON r.circuitId = c.circuitId JOIN results rs ON r.raceId = rs.raceId JOIN drivers d ON rs.driverId = d.driverId JOIN constructors cn ON rs.constructorId = cn.constructorId WHERE r.name LIKE '{search_term}%' AND rs.position IN (1, 2, 3)"
        total_count_query = f"SELECT COUNT(*) FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name LIKE '{search_term}%'"
    else:
        query = f"SELECT r.name, r.year, r.date, r.round, c.name, c.country, c.lat, c.lng, c.url, c.location, r.raceId FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE LENGTH(r.name) > 0"
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

    query += f" LIMIT {RESULTS_PER_PAGE} OFFSET {offset}"
    race_results_query += f" LIMIT {RESULTS_PER_PAGE} OFFSET {offset}"
    
    results = db.execute(query).fetchall()
    race_results = db.execute(race_results_query).fetchall()
    race_results = sorted(race_results, key=lambda x: (x[-1], x[3]))


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