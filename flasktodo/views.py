import functools

from flask import (
    Blueprint, request, url_for, render_template, flash, redirect, g, session
)
from werkzeug.security import generate_password_hash, check_password_hash

from flasktodo import forms, db, models

bp = Blueprint('home', __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = models.User.query.filter_by(id=user_id).first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        print('g.user in login_required is ', g.user)
        if g.user is None:
            flash("Not logged in")
            return redirect(url_for('home.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/')
@login_required
def home():
    return render_template('home.html',
                           message='hello world!',
                           users=models.User.query.all(),
                           passwords=db.session.query(models.User.password_hash).all()
                           )


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        if check_login(form.username.data, form.password.data):
            flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            session.clear()
            session['user_id'] = get_user(form.username.data).id
            # g.user = get_user(form.username.data).id
            # print('g.user set to ', g.user)
            return redirect(url_for('home.home'))
        else:
            flash('Incorrect login')
    return render_template('login.html', form=form)


def get_user(username):
    return models.User.query.filter_by(username=username).first()


def check_login(username, password):
    user = get_user(username)
    print(user)
    return user and check_password_hash(user.password_hash, password)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        # flash('Registration requested for user {}'.format(form.username.data))
        if models.User.query.filter_by(username=form.username.data).first():
            flash('User already exists')
            redirect(url_for('home.register'))
        else:
            db.session.add(models.User(username=form.username.data,
                                       password_hash=generate_password_hash(form.password.data)))
            db.session.commit()
            return redirect(url_for('home.home'))

    return render_template('register.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.login'))
