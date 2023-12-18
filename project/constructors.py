from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from project.db import get_db
from flask_paginate import Pagination, get_page_args

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
        'constructors/constructors.html', 
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

    query = ('SELECT r.year, r.name as r_name, c.name as c_name,   cr.points, cr.raceId ' 
             'FROM constructor_results cr JOIN races r ON r.raceId = cr.raceId JOIN circuits c ON r.circuitId = c.circuitId '
             f'WHERE cr.constructorId = {const_id} ORDER BY cr.points DESC LIMIT 10')
    
    cursor= con.cursor()
    cursor.execute(query)
    raceInfos = cursor.fetchall()

    print(const_id)

    second_query = f"SELECT results.driverId, results.points, results.position FROM results WHERE constructorId = {const_id} AND raceId IN (SELECT raceId FROM constructor_results WHERE constructorId = {const_id})"
    
    cursor.execute(second_query)
    race_results = cursor.fetchall()

    return render_template(
        'constructors/constructor_details.html', 
        constructorRef=constructorRef,
        const_name = const_name,
        raceInfos = raceInfos,
        race_results = race_results
    )

@bp.route('/constructors/create', methods=('GET', 'POST'))
#@login_required
def create():
    if request.method == 'POST':
        constructorId = request.form['constructorId']
        constructorRef = request.form['constructorRef']
        name = request.form['name']
        nationality = request.form['nationality']
        url = request.form['url']
        error = None


        if not constructorId or not constructorRef or not name or not nationality or not url:
            error = 'All fields are required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO constructors (constructorId, constructorRef, name, nationality, url)'
                ' VALUES (?, ?, ?, ?, ?)',
                (constructorId, constructorRef, name, nationality, url)
            )
            db.commit()
            return redirect(url_for('constructors.index'))

    return render_template('constructors/create.html')

@bp.route('/constructors/update', methods=['POST'])
def update():
    print("Update func")
    try:
        # Get the data from the JSON request body
        updated_data = request.json.get('data', [])
        db = get_db()
        # Perform the update operation in your database
        for data_entry in updated_data:
            constructorId = data_entry.get('constructorId')
            constructorRef = data_entry.get('constructorRef')
            name = data_entry.get('name')
            nationality = data_entry.get('nationality')
            url = data_entry.get('url')

            query = ('UPDATE drivers SET constructorRef = ?, name = ?, nationality = ?, url = ? '
                     ' WHERE constructorId = ?')
            db.execute(query, (constructorRef, name, nationality, url, constructorId))
            db.commit()

        # Return a response (you can customize the response based on your needs)
        return jsonify({'message': 'Update successful'}), 200
    except Exception as e:
        # Handle exceptions as needed
        print('Error updating backend:', e)
        return jsonify({'error': 'Internal Server Error'}), 500
