from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from project.db import get_db
from project.auth import login_required
from math import ceil


bp = Blueprint('constructors', __name__)

RESULTS_PER_PAGE = 10

@bp.route('/constructors/')
def index():
    con = get_db()
    cursor = con.cursor()
    page = request.args.get('page', default=1, type=int)
    filter_name = request.args.get('filter_name', '')

    unique_nationalities = con.execute("SELECT DISTINCT nationality FROM constructors ORDER BY nationality").fetchall()
    
    offset = (page - 1) * RESULTS_PER_PAGE


    base_query = "SELECT * FROM constructors WHERE 1 = 1 "
    total_count_query = "SELECT COUNT(*) FROM constructors WHERE 1 = 1 "
    nationality_dropdown = request.args.get('nationality_dropdown', '')

    if filter_name:
        base_query += f"AND lower(name) LIKE '%{filter_name}%'"
        total_count_query += f"AND lower(name) LIKE '%{filter_name}%'"
    if nationality_dropdown:
        base_query += f"AND lower(nationality) LIKE '%{nationality_dropdown}%'"
        total_count_query += f"AND lower(nationality) LIKE '%{nationality_dropdown}%'"

    query = base_query + f" LIMIT {RESULTS_PER_PAGE} OFFSET {offset}"
    
    print(query)
    cursor.execute(query)
    constructors = cursor.fetchall()

    # Count total results for pagination
    total_count = cursor.execute(total_count_query).fetchone()[0]
    total_pages = ceil(total_count / RESULTS_PER_PAGE)

    return render_template(
        'constructors/constructors.html', 
        constructors=constructors, 
        filter_name=filter_name, 
        nationality_dropdown=nationality_dropdown, 
        unique_nationalities=unique_nationalities,
        page=page, 
        total_pages=total_pages,
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

    query = ('SELECT r.year, cr.raceId, r.name as r_name, c.name as c_name,   cr.points  ' 
             'FROM constructor_results cr JOIN races r ON r.raceId = cr.raceId JOIN circuits c ON r.circuitId = c.circuitId '
             f'WHERE cr.constructorId = {const_id} ORDER BY cr.points DESC LIMIT 10')
    
    cursor= con.cursor()
    cursor.execute(query)
    raceInfos = cursor.fetchall()

    race_ids_query = ('SELECT cr.raceId  ' 
                    'FROM constructor_results cr JOIN races r ON r.raceId = cr.raceId JOIN circuits c ON r.circuitId = c.circuitId '
                    f'WHERE cr.constructorId = {const_id} ORDER BY cr.points DESC LIMIT 10')

    print(const_id)

    cursor.execute(race_ids_query)
    race_ids = cursor.fetchall()

    #To get the raceIds that have yielded the best results
    raceIds = ""
    for row in race_ids:
        for x in row:
            raceIds = raceIds + str(x) + ", " 
    raceIds = raceIds.rstrip(', ')
    print(raceIds)

    second_query = f"SELECT results.raceId, results.driverId, results.points, results.position FROM results WHERE constructorId = {const_id} AND raceId IN ({raceIds})"
    print(second_query)
    third_query = f"SELECT raceId FROM constructor_results WHERE constructorId = {const_id}"

    cursor.execute(second_query)
    race_results = cursor.fetchall()

    for row in race_results:
        for x in row:
            print(str(x), end=" | ")
        print("")

    return render_template(
        'constructors/constructor_details.html', 
        constructorRef=constructorRef,
        const_name = const_name,
        raceInfos = raceInfos,
        #race_results = race_results
    )

@bp.route('/constructors/create', methods=('GET', 'POST'))
@login_required
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
@login_required
def update():
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

            query = ('UPDATE constructors SET constructorRef = ?, name = ?, nationality = ?, url = ? WHERE constructorId = ? ')
            db.execute(query, (constructorRef, name, nationality, url, constructorId))
            db.commit()

        # Return a response (you can customize the response based on your needs)
        return jsonify({'message': 'Update successful'}), 200
    except Exception as e:
        # Handle exceptions as needed
        print('Error updating backend:', e)
        return jsonify({'error': 'Internal Server Error'}), 500

@bp.route('/constructors/delete', methods=('GET', 'POST', 'DELETE'))
@login_required
def delete():
    if request.method == 'DELETE':
        try:
            print("bfkdfn")
            constructorIds = request.json.get('constructorIds', [])
            if constructorIds:
                for const_id in constructorIds:
                    print(const_id)
            db = get_db()
            query = f'DELETE FROM constructors WHERE constructorId in ("'
            for const_id in constructorIds:
                if const_id != constructorIds[0]:
                    query += '", "'
                query += f"{const_id}"
            query += '")'
            print(query)
            db.execute(query, )
            db.commit()

            return jsonify({"message": "Constructor deleted successfully"}), 200
        except ValueError:
            return jsonify({"error": "Invalid constructorId parameter"}), 400 #silinebilir
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    else:
        return jsonify({"error": "Method not allowed"}), 405

