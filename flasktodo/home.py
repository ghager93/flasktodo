from flask import (
    Blueprint, request, url_for, render_template
)

from . import forms

bp = Blueprint('home', __name__)

@bp.route('/')
def home():
    return render_template('home.html', message='hello world!')

@bp.route('/login')
def login():
    form = forms.LoginForm()
    return render_template('login.html', form=form)