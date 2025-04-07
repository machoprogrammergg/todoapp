from flask import Blueprint, json, render_template, request, flash, redirect, url_for  # Import necessary Flask functions
from flask_login import login_required, current_user  # Import login_required for protecting routes and current_user for accessing logged-in user's data
from website import db  # Import db object to interact with the database
from .models import TaskList, UserAccount  # Import TaskList and UserAccount models

import datetime as time  # Import datetime for managing task timestamps
views = Blueprint('views', __name__)  # Define the 'views' blueprint for organizing routes

# Home route: Only accessible by logged-in users
@views.route('/')
@login_required  # Protect this route to ensure only logged-in users can access it
def home():
    return render_template('home.html', user=current_user)  # Render the home page template, passing the current logged-in user

# New Task route: Handles creating a new task (both GET and POST methods)
@views.route('/new-task', methods=['GET', 'POST'])
def newTask():
    if request.method == 'POST':  # If the request method is POST (form submission)
        # Get form data
        new_title = request.form.get('title')
        new_note = request.form.get('note')
        
        # Generate current timestamp for the task
        current_time = time.datetime.now()
        stamp = f'{current_time.strftime("%A, %d %B")}'  # Format the date

        # Validate the task title
        if len(new_title) < 4:
            flash('Task title should be greater than 4 characters', category='error')  # Show error if title is too short
        elif len(new_title) == 0:
            flash('Please enter a task title', category='error')  # Show error if title is empty
        elif len(new_note) == 0:
            new_note = f'No note created'  # Default note if no note is provided
            # Create and save new task to the database
            new_task = TaskList(title=new_title, note=new_note, user_id=current_user.id, time_stamp=stamp, completed=False)
            current_user.task_count += 1  # Increment the task count for the user
            db.session.add(new_task)  # Add the task to the session
            db.session.commit()  # Commit the transaction to the database
            return redirect(url_for('views.home'))  # Redirect to the home page after successful creation
        else:
            # Create and save new task with note to the database
            new_task = TaskList(title=new_title, note=new_note, user_id=current_user.id, time_stamp=stamp, completed=False)
            current_user.task_count += 1  # Increment the task count for the user
            db.session.add(new_task)  # Add the task to the session
            db.session.commit()  # Commit the transaction to the database
            return redirect(url_for('views.home'))  # Redirect to the home page after successful creation

    return render_template('new-task.html', user=current_user)  # Render the 'new-task.html' template for GET requests

# Delete Task route: Deletes a task by its ID
@views.route('/delete-task/<int:id>')  # Capture the task ID from the URL
def deleteTask(id):
    task = TaskList.query.get(id)  # Retrieve the task by ID from the database
    if task:  # If the task exists
        if task.user_id == current_user.id:  # Check if the task belongs to the logged-in user
            db.session.delete(task)  # Delete the task from the database
            current_user.task_count -= 1  # Decrease the task count for the user
            db.session.commit()  # Commit the transaction to the database
    return redirect(url_for('views.home'))  # Redirect to the home page after deletion

# Mark Task as Done route: Marks a task as completed
@views.route('/mark-as-done/<int:id>')  # Capture the task ID from the URL
def markAsDone(id):
    task = TaskList.query.get(id)  # Retrieve the task by ID from the database
    if task:  # If the task exists
        if task.user_id == current_user.id:  # Check if the task belongs to the logged-in user
            task.completed = True  # Mark the task as completed
            db.session.commit()  # Commit the transaction to the database
    return redirect(url_for('views.home'))  # Redirect to the home page after marking as done
