from flask import Blueprint, json, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website import db
from .models import TaskList, UserAccount

import datetime as time
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/new-task', methods=['GET', 'POST'])
def newTask():
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_note = request.form.get('note')
        current_time = time.datetime.now()
        stamp = f'{current_time.strftime('%A' + ', %d ' + '%B')}  {current_time.strftime('%H' + ':' + '%M')}'

        if len(new_title) < 4:
            flash('Task title should be greater than 4 characters', category='error')
        elif len(new_title) == 0:
            flash('Please enter a task title', category='error')
        elif len(new_note) == 0 :
            new_note = f'No note created'
            new_task = TaskList(title=new_title, note=new_note, user_id=current_user.id, time_stamp=stamp, completed=False)
            current_user.task_count += 1
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('views.home'))
        else:
            new_task = TaskList(title=new_title, note=new_note, user_id=current_user.id, time_stamp=stamp, completed=False)
            current_user.task_count += 1
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template('new-task.html', user=current_user,)

@views.route('/delete-task/<int:id>')
def deleteTask(id):  
    task = TaskList.query.get(id)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            current_user.task_count -= 1
            db.session.commit()
    return redirect(url_for('views.home'))


@views.route('/mark-as-done/<int:id>')
def markAsDone(id):
    task = TaskList.query.get(id)
    if task:
        if task.user_id == current_user.id:
            task.completed = True
            db.session.commit()
    return redirect(url_for('views.home'))
