from flask import (
    Blueprint, request, url_for, render_template, flash, redirect
)

from flasktodo import forms, db, models

bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    return render_template('home.html', message='hello world!', users=models.User.query.all())


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home.home'))
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('Registration requested for user {}'.format(form.username.data))
        return redirect(url_for('home.home'))

    return render_template('register.html', form=form)

