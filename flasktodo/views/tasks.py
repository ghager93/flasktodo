from flask import (
    Blueprint, request, url_for, render_template, flash, redirect, g, session
)
from werkzeug.exceptions import abort

from flasktodo import forms, db, models
from flasktodo.views.auth import login_required

bp = Blueprint('tasks', __name__)

#
# @bp.route('/')
# @login_required
# def index():
#     return render_template('home.html',
#                            message='hello world!',
#                            users=models.User.query.all(),
#                            passwords=db.session.query(models.User.password_hash).all()
#                            )


@bp.route('/')
@login_required
def index():
    return render_template('task_index.html', tasks=models.Task.query.all())


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = forms.CreateTaskForm()
    if form.validate_on_submit():
        db.session.add(models.Task(user_id=g.user.id,
                                   title=form.title.data,
                                   body=form.body.data,
                                   is_done=False
                                   ))
        db.session.commit()
        return redirect(url_for('tasks.index'))

    return render_template('create_task.html', form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    task = get_task(id)
    form = forms.EditTaskForm()
    if request.method == "GET":
        form.title.data = task.title
        form.body.data = task.body
    if form.validate_on_submit():
        task.title = form.title.data
        task.body = form.body.data
        db.session.commit()
        return redirect(url_for('tasks.index'))

    return render_template('edit_task.html', form=form)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    models.Task.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('tasks.index'))


def get_task(id):
    task = models.Task.query.filter_by(id=id).first()
    if task:
        return task
    else:
        abort(404, f"task id {id} not found")
