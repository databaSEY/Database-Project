from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from project.db import get_db

bp = Blueprint('drivers', __name__)

@bp.route('/drivers')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT d.driverId, d.driverRef, d.forename, d.surname, d.nationality'
        ' FROM drivers d'
        ' ORDER BY driverId'
    ).fetchall()
    print(posts[0]) # test amaçlı
    return render_template('drivers.html', posts=posts)