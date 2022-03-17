from flask import (
    Blueprint, request, url_for, render_template, flash, redirect, g, session
)

from flasktodo import forms, db, models
from flasktodo.views.auth import login_required


bp = Blueprint('posts', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('home.html',
                           message='hello world!',
                           users=models.User.query.all(),
                           passwords=db.session.query(models.User.password_hash).all()
                           )
