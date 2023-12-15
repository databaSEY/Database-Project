from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from project.db import get_db

bp = Blueprint('drivers', __name__)

@bp.route('/drivers', methods=['GET'])
def index():
    # Get the current page and drivers per page from the URL parameters
    page = request.args.get('page', default=1, type=int)
    drivers_per_page = request.args.get('drivers_per_page', default=10, type=int)

    # Calculate the offset to retrieve the appropriate range of drivers from the database
    offset = (page - 1) * drivers_per_page

    search_term = request.args.get('search', '')
    
    db = get_db()
    total_drivers = db.execute('SELECT COUNT(*) FROM drivers WHERE forename LIKE ?', (f'{search_term}%',)).fetchone()[0]
    total_pages = total_drivers // drivers_per_page

    if search_term:
        # If a search term is provided, filter the results based on the first name
        query = (
            'SELECT d.driverId, d.driverRef, d.forename, d.surname, d.nationality'
            ' FROM drivers d'
            ' WHERE d.forename LIKE ?'
            ' ORDER BY d.driverId'
            ' LIMIT ? OFFSET ?'
        )
        search_term_with_percent = f'{search_term}%'
        posts = db.execute(query, (search_term_with_percent, drivers_per_page, offset)).fetchall()
    else:
        # If no search term, retrieve all drivers
        query = (
            'SELECT d.driverId, d.driverRef, d.forename, d.surname, d.nationality'
            ' FROM drivers d'
            ' ORDER BY d.driverId'
            ' LIMIT ? OFFSET ?'
        )
        posts = db.execute(query, (drivers_per_page, offset)).fetchall()


    return render_template('drivers/index.html', posts=posts, total_drivers = total_drivers, total_pages = total_pages, page=page, drivers_per_page=drivers_per_page)


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