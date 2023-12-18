from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from project.db import get_db


bp = Blueprint('constructors', __name__)

@bp.route('/constructors/')
def index():
    con = get_db()
    cursor = con.cursor()
    filter_name = request.args.get('filter_name', '')
    filter_nationality = request.args.get('filter_nationality', '')

    unique_nationalities = con.execute("SELECT DISTINCT nationality FROM constructors ORDER BY nationality").fetchall()
    
    base_query = "SELECT * FROM constructors WHERE 1 = 1 "
    nationality_dropdown = request.args.get('nationality_dropdown', '')

    if filter_nationality:
        base_query += f"AND lower(name) LIKE '%{filter_nationality}%'"
    if nationality_dropdown:
        base_query += f"AND lower(nationality) LIKE '%{nationality_dropdown}%'"


    query = base_query
    
    print(query)
    cursor.execute(query)
    constructors = cursor.fetchall()

    # Count total results for pagination
    total_results = con.execute(f"SELECT COUNT(*) FROM ({base_query})").fetchone()[0]

    return render_template(
        'constructors.html', 
        constructors=constructors, 
        filter_name=filter_name, 
        nationality_dropdown=nationality_dropdown, 
        unique_nationalities=unique_nationalities,
    )

@bp.route('/constructors/<string:constructorRef>/details')
def details(constructorRef):
    # Retrieve details for the specified constructorRef
    # Render the details page with the retrieved data
    con = get_db()
    name_query = f"SELECT name FROM constructors WHERE constructorRef = '{constructorRef}'"
    const_name = con.execute(name_query).fetchone()[0]
    id_query = f"SELECT constructorId FROM constructors WHERE constructorRef = '{constructorRef}'"
    const_id = con.execute(id_query).fetchone()[0]

    #SELECT * FROM constructor_results WHERE constructorId=1 ORDER BY points DESC LIMIT 10

    query = f"SELECT raceId, points FROM constructor_results WHERE constructorId = {const_id} ORDER BY points DESC LIMIT 10"
    cursor= con.cursor()
    cursor.execute(query)
    raceInfos = cursor.fetchall()

    print(const_id)

    second_query = f"SELECT results.driverId, results.points, results.position FROM results WHERE constructorId = {const_id} AND raceId IN (SELECT raceId FROM constructor_results WHERE constructorId = {const_id})"
    
    cursor.execute(second_query)
    race_results = cursor.fetchall()

    return render_template(
        'constructor_details.html', 
        constructorRef=constructorRef,
        const_name = const_name,
        raceInfos = raceInfos,
        race_results = race_results
    )

