import os
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app
from flaskr.auth import login_required, s2_required, s3_required
from flaskr.db import get_db
from flaskr.projects import get_project, get_project_users
from flaskr.auth import get_user, allowed_file
from flaskr.files import deleteTicketFiles
from werkzeug.utils import secure_filename

bp = Blueprint('tickets', __name__)


def get_ticket(id):
    ticket = get_db().execute(
        "SELECT * FROM tickets WHERE ticket_id == ?", (id,)
    ).fetchone()

    return ticket

def get_user_tickets(user_id):
    tickets = get_db().execute(
        "SELECT * FROM tickets WHERE assigned_user_id == ?", (user_id,)
    ).fetchall()

    return tickets

def get_comments(ticket_id):
    comments = get_db().execute(
        "SELECT * FROM comments WHERE ticket_id = ?", (ticket_id,)
    ).fetchall()

    return comments

def get_changelog(ticket_id):
    changelog = get_db().execute(
        "SELECT * FROM ticket_changelog WHERE ticket_id = ?", (ticket_id,)
    ).fetchall()

    return changelog

def get_files(ticket_id):
    files = get_db().execute(
        "SELECT * FROM attachments WHERE ticket_id = ?", (ticket_id,)
    ).fetchall()

    return files


@bp.route('/myTickets')
@login_required
def myTickets():
    tickets = get_user_tickets(g.user['user_id'])
    projectTitles = []
    for ticket in tickets:
        proj = get_project(ticket['project_id'])
        projectTitles.append(proj['title'])

    return render_template('tickets/myTickets.html', g = g, tickets = tickets, projectTitles = projectTitles, ticketCount = len(tickets))

@bp.route('/tickets/<int:ticket_id>/view', methods=('GET', 'POST'))
@login_required
def viewTicket(ticket_id):
    ticket = get_ticket(ticket_id)
    error = None

    if request.method == 'POST':
        db = get_db()
        
        if 'comment' in request.form:
            comment_body = request.form['commentBody']
            db.execute(
                "INSERT INTO comments (comment_body, author_id, author_username, ticket_id) VALUES (?, ?, ?, ?)", (comment_body, g.user['user_id'], g.user['username'], ticket_id)
            )
            flash('comment added')
            db.commit()
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No selected File')
                return redirect(url_for('tickets.viewTicket', ticket_id=ticket))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(ticket_id))
                try:
                    os.makedirs(path)
                except:
                    pass
                file.save(os.path.join(path, filename))
                flash('file successfully uploaded')

                db.execute(
                    "INSERT INTO attachments (filename, author_id, author_username, ticket_id) VALUES (?, ?, ?, ?)", (filename, g.user['user_id'], g.user['username'], ticket_id)
                )
                db.commit()
            else:
                flash('file type not allowed')
    
    comments = get_comments(ticket_id)
    changelog = get_changelog(ticket_id)
    files = get_files(ticket_id)


    return render_template('tickets/viewTicket.html', g = g, ticket = ticket, comments = comments[::-1], commentsLength = len(comments), changelog = changelog[::-1], changelogLength = len(changelog), files = files, fileCount = len(files))

@bp.route('/projects/<int:project_id>/tickets/<int:ticket_id>/update', methods=('GET', 'POST'))
@login_required
@s2_required
def updateTicket(project_id, ticket_id):
    ticket = get_ticket(ticket_id)
    project = get_project(project_id)
    project_users = get_project_users(project_id)
    error = None

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        assigned = request.form['assigned_user_id'].split(';')
        assigned_user_id = assigned[0]
        assigned_username = assigned[-1]

        if not title or not description:
            error = 'title and description required'
            flash(error)
        
        if not error:
            db = get_db()

            changedProperties = []
            properties = [('title', title), ('description', description), ('priority', priority), ('assigned_username', assigned_username)]
            for property in properties:
                if property[1] != ticket[property[0]]:
                    changedProperties.append((property[0], ticket[property[0]], property[1]))
        
            for property in changedProperties:
                db.execute(
                    "INSERT INTO ticket_changelog (ticket_id, property, old_value, new_value, author_id, author_username) VALUES (?, ?, ?, ?, ?, ?)", (ticket_id, property[0], property[1], property[2], g.user['user_id'], g.user['username'])
                )
                db.commit()



            db.execute(
                "UPDATE tickets SET title = ?, description = ?, priority = ?, assigned_user_id = ?, assigned_username = ?"
                "WHERE ticket_id = ?", (title, description, priority, assigned_user_id, assigned_username, ticket_id)
            )
            db.commit()
            flash('ticket updated')
            return redirect(url_for('tickets.viewTicket', ticket_id = ticket_id))


    return render_template('tickets/updateTicket.html', g = g, project = project, ticket = ticket, project_users = project_users)

@bp.route('/projects/<int:project_id>/createTicket', methods=('GET', 'POST'))
@login_required
@s2_required
def createTicket(project_id):
    project = get_project(project_id)
    project_users = get_project_users(project_id)
    error = None

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        assigned = request.form['assigned'].split(';')
        assigned_user_id = assigned[0]
        assigned_username = assigned[-1]

        if not title or not description:
            error = 'title and description required'
            flash(error)
        
        if not error:
            db = get_db()
            db.execute(
                "INSERT INTO tickets (title, description, priority, author_id, author_username, project_id, assigned_user_id, assigned_username)"
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (title, description, priority, g.user['user_id'], g.user['username'], project_id, assigned_user_id, assigned_username)
            )
            db.commit()
            flash('ticket created')
            return redirect(url_for('projects.viewProject', project_id = project_id))


    return render_template('tickets/createTicket.html', g = g, project = project, project_users = project_users)

@bp.route('/projects/<int:project_id>/tickets/<int:ticket_id>/deleteTicket')
@login_required
@s2_required
def deleteTicket(project_id, ticket_id):
    db = get_db()
    db.execute(
        "DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,)
    )
    db.execute(
        "DELETE FROM attachments WHERE ticket_id = ?", (ticket_id,)
    )
    db.commit()

    deleteTicketFiles(ticket_id)
    flash('ticket deleted')

    return redirect(url_for('projects.viewProject', project_id=project_id))