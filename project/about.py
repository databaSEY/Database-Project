from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
#from project.db import get_db
#from project.auth import login_required
#from math import ceil

bp = Blueprint('about', __name__)

@bp.route('/about/')
def index():
    return render_template('about.html')
