from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from project.auth import login_required
from project.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    db = get_db()
    top_drivers_query = (
        'SELECT '
        ' ROW_NUMBER() OVER (ORDER BY SUM(res.points) DESC) AS row_num, '
         ' d.forename, '
         ' d.surname,'
         ' SUM(res.points) as sum_of_points'
         ' FROM drivers d'
  		 ' JOIN results res ON res.driverId=d.driverId'
         ' GROUP BY d.driverId'
         ' ORDER BY sum_of_points desc'
         ' LIMIT 5'
    )
    top_constructors_query = (
       ' SELECT '
        ' ROW_NUMBER() OVER (ORDER BY SUM(cs.wins) DESC) AS row_num,'
        ' c.name,'
        ' c.nationality,'
        ' SUM(cs.wins) AS sum_of_wins'
        ' FROM constructor_standings cs'
        ' JOIN constructors c ON c.constructorId = cs.constructorId '
        ' GROUP BY cs.constructorId'
        ' ORDER BY sum_of_wins DESC'
        ' LIMIT 5'
    )
    last_races_query = (
        'SELECT'
        ' ROW_NUMBER() OVER (ORDER BY date) AS row_num,'
        ' r.name,'
        ' r.date '
        ' FROM races r'
        ' ORDER BY r.date DESC'
        ' LIMIT 5'
    )
    top_drivers = db.execute( top_drivers_query, ).fetchall()
    top_constructors = db.execute( top_constructors_query, ).fetchall()
    last_races = db.execute( last_races_query, ).fetchall()
    return render_template('home/index.html', top_drivers=top_drivers, top_constructors=top_constructors, last_races=last_races)
