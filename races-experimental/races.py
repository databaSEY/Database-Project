from flask import Flask, render_template, request
import sqlite3
from math import ceil

app = Flask(__name__)

RESULTS_PER_PAGE = 10
def get_search_results(search_term, year_filter, country_filter, page):
    offset = (page - 1) * RESULTS_PER_PAGE
    conn = sqlite3.connect('Formula1.sqlite')
    cursor = conn.cursor()

    # Base query with search term
    query = f"SELECT r.name, r.year, r.date, r.round, c.name, c.country, c.lat, c.lng, c.url , c.location, r.raceId FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name LIKE '{search_term}%'"

    # Add filters for year and country
    if year_filter:
        query += f" AND r.year = {year_filter}"
    if country_filter:
        query += f" AND c.country = '{country_filter}'"

    query += f" LIMIT {RESULTS_PER_PAGE} OFFSET {offset}"
    
    cursor.execute(query)
    results = cursor.fetchall()
    # Race results query
    race_results_query = f"SELECT d.forename, d.surname, d.code, rs.position, rs.time, cn.name, r.raceId FROM races r JOIN circuits c ON r.circuitId = c.circuitId JOIN results rs ON r.raceId = rs.raceId JOIN drivers d ON rs.driverId = d.driverId JOIN constructors cn ON rs.constructorId = cn.constructorId WHERE r.name LIKE '{search_term}%' AND rs.position IN (1, 2, 3)"
    # Add filters to race results query
    if year_filter:
        race_results_query += f" AND r.year = {year_filter}"
    if country_filter:
        race_results_query += f" AND c.country = '{country_filter}'"
    race_results_query += f" LIMIT {RESULTS_PER_PAGE} OFFSET {offset}"
    
    cursor.execute(race_results_query)
    race_results = cursor.fetchall()
    race_results = sorted(race_results, key=lambda x: ( x[-1], x[3]))

    # Count the total number of results for pagination
    total_count_query = f"SELECT COUNT(*) FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name LIKE '{search_term}%'"
    # Add filters to total count query
    if year_filter:
        total_count_query += f" AND r.year = {year_filter}"
    if country_filter:
        total_count_query += f" AND c.country = '{country_filter}'"

    cursor.execute(total_count_query)
    total_count = cursor.fetchone()[0]

    # Retrieve distinct years and countries
    distinct_years_query = "SELECT DISTINCT year FROM races"
    cursor.execute(distinct_years_query)
    distinct_years = [str(year[0]) for year in cursor.fetchall()]

    distinct_countries_query = "SELECT DISTINCT country FROM circuits"
    cursor.execute(distinct_countries_query)
    distinct_countries = [country[0] for country in cursor.fetchall()]

    conn.close()

    # Calculate the total number of pages
    total_pages = ceil(total_count / RESULTS_PER_PAGE)

    return results, race_results, total_pages, distinct_years, distinct_countries

@app.route('/race')
def index():
    search_term = request.args.get('search', default='', type=str)
    year_filter = request.args.get('year', default='', type=str)
    country_filter = request.args.get('country', default='', type=str)
    page = request.args.get('page', default=1, type=int)

    results, race_results, total_pages, distinct_years, distinct_countries = get_search_results(search_term, year_filter, country_filter, page)
    return render_template('races.html', search_term=search_term, results=results, race_results=race_results, page=page, total_pages=total_pages,
                           distinct_years=distinct_years, distinct_countries=distinct_countries,
                           selected_year=year_filter, selected_country=country_filter)

if __name__ == '__main__':
    app.run(debug=True)
