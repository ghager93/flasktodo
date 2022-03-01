from flask import (
    Blueprint, request, url_for, render_template
)

bp = Blueprint('home', __name__)

@bp.route('/')
def home():
    return render_template('home.html', message='hello world!')