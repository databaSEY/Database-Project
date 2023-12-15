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
    query = f"SELECT r.name, r.year, c.name AS circuit_name, c.country AS circuit_country, c.lat, c.lng, c.url FROM races r JOIN circuits c ON r.circuitId = c.circuitId WHERE r.name LIKE '{search_term}%'"

    # Add filters for year and country
    if year_filter:
        query += f" AND r.year = {year_filter}"
    if country_filter:
        query += f" AND c.country = '{country_filter}'"

    query += f" LIMIT {RESULTS_PER_PAGE} OFFSET {offset}"

    cursor.execute(query)
    results = cursor.fetchall()

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

    return results, total_pages, distinct_years, distinct_countries

@app.route('/')
def index():
    search_term = request.args.get('search', default='', type=str)
    year_filter = request.args.get('year', default='', type=str)
    country_filter = request.args.get('country', default='', type=str)
    page = request.args.get('page', default=1, type=int)

    results, total_pages, distinct_years, distinct_countries = get_search_results(search_term, year_filter, country_filter, page)

    return render_template('races.html', search_term=search_term, results=results, page=page, total_pages=total_pages,
                           distinct_years=distinct_years, distinct_countries=distinct_countries,
                           selected_year=year_filter, selected_country=country_filter)

if __name__ == '__main__':
    app.run(debug=True)
