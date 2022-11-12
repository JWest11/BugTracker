from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.auth import get_user, login_required, s2_required, s3_required
from flaskr.projects import get_project, get_project_users, get_all_projects, get_project_tickets
from flaskr.tickets import get_user_tickets, get_ticket

bp = Blueprint('teams', __name__)

def get_all_users():
    users = get_db().execute(
        "SELECT * FROM users"
    ).fetchall()

    return users

def get_users_projects(user_id):
    db = get_db()
    ids = db.execute(
        "SELECT * FROM users_projects WHERE user_id = ?", (user_id,)
    ).fetchall()

    projects = []
    for row in ids:
        projects.append(
            db.execute(
                "SELECT * FROM projects WHERE project_id = ?", (row['project_id'],)
            ).fetchone()
        )
    
    return projects

def set_secutiry_level(user_id, security_level):
    db = get_db()
    db.execute(
        "UPDATE users SET security_level = ? WHERE user_id = ?", (security_level, user_id)
    )
    db.commit()
    


@bp.route('/projects/<int:project_id>/updateTeam')
@login_required
@s2_required
def updateProjectTeam(project_id):
    all_users = get_all_users()
    assigned_users = get_project_users(project_id)
    assigned_ids = set()
    for user in assigned_users:
        assigned_ids.add(user['user_id'])
    unassigned_users = []
    for user in all_users:
        if user['user_id'] not in assigned_ids:
            unassigned_users.append(user)
    project = get_project(project_id)

    return render_template('teams/updateProjectTeam.html',g = g, unassigned_users = unassigned_users, assigned_users = assigned_users, project = project)

@bp.route('/projects/<int:project_id>/addTeamMember/<int:user_id>')
@login_required
@s2_required
def addTeamMember(project_id, user_id):
    db = get_db()
    db.execute(
        "INSERT INTO users_projects (user_id, project_id) VALUES (?, ?)", (user_id, project_id)
    )
    db.commit()
    flash('project assigned')

    return redirect(url_for('teams.updateProjectTeam', project_id=project_id))

@bp.route('/projects/<int:project_id>/removeTeamMember/<int:user_id>')
@login_required
@s2_required
def removeTeamMember(project_id, user_id):
    db = get_db()
    db.execute(
        "DELETE FROM users_projects WHERE user_id = ? AND project_id = ?", (user_id, project_id)
    )
    db.commit()
    flash('project unassigned')

    return redirect(url_for('teams.updateProjectTeam', project_id=project_id))

@bp.route('/projects/<int:project_id>/addTeamMember2/<int:user_id>')
@login_required
@s2_required
def addTeamMember2(project_id, user_id):
    db = get_db()
    db.execute(
        "INSERT INTO users_projects (user_id, project_id) VALUES (?, ?)", (user_id, project_id)
    )
    db.commit()
    flash('project assigned')

    return redirect(url_for('teams.manageUser', user_id=user_id))

@bp.route('/projects/<int:project_id>/removeTeamMember2/<int:user_id>')
@login_required
@s2_required
def removeTeamMember2(project_id, user_id):
    db = get_db()
    db.execute(
        "DELETE FROM users_projects WHERE user_id = ? AND project_id = ?", (user_id, project_id)
    )
    db.commit()
    flash('project unassigned')

    return redirect(url_for('teams.manageUser', user_id=user_id))

@bp.route('/teams', methods=('GET', 'POST'))
@login_required
@s2_required
def teams():

    if request.method == 'POST':
        newSecurity = request.form['securityLevel']
        userId = request.form['user_id']
        set_secutiry_level(userId, newSecurity)

    all_users = get_all_users()
    completeUsers = []
    for user in all_users:
        tickets = get_user_tickets(user['user_id'])
        projects = get_users_projects(user['user_id'])
        projectString = ""
        for project in projects:
            projectString += project['title'] + ". "

        completeUsers.append({'user': user, 'ticketCount': len(tickets), 'projects': projectString})

    return render_template('teams/manageTeams.html', g = g, completeUsers = completeUsers, userCount = len(completeUsers))

@bp.route('/user/<int:user_id>', methods=('GET', 'POST'))
@login_required
@s3_required
def manageUser(user_id):

    if request.method == 'POST':
        newSecurity = request.form['securityLevel']
        set_secutiry_level(user_id, newSecurity)
        flash('security level updated')

    user = get_user(user_id)
    all_projects = get_all_projects()
    users_projects = get_users_projects(user_id)
    assigned_project_ids = set()
    for project in users_projects:
        assigned_project_ids.add(project['project_id'])
    unassigned_projects = []
    for project in all_projects:
        if project['project_id'] not in assigned_project_ids:
            unassigned_projects.append(project)
    tickets = get_user_tickets(user_id)
    assigned_ticket_ids = set()
    for ticket in tickets:
        assigned_ticket_ids.add(ticket['ticket_id'])
    available_tickets = []
    for project in users_projects:
        proj = get_project_tickets(project['project_id'])
        for tick in proj:
            if tick['ticket_id'] not in assigned_ticket_ids:
                available_tickets.append(tick)

    return render_template('teams/manageUser.html', g = g, user = user, unassigned_projects = unassigned_projects, users_projects = users_projects, tickets = tickets, available_tickets = available_tickets)


@bp.route('/ticket/<int:ticket_id>/user/<int:user_id>/unassign')
@login_required
@s3_required
def unassignTicket(ticket_id, user_id):
    db = get_db()
    ticket = get_ticket(ticket_id)
    db.execute(
        "INSERT INTO ticket_changelog (ticket_id, property, old_value, new_value, author_id, author_username) VALUES (?, ?, ?, ?, ?, ?)", (ticket_id, 'assigned_username', ticket['assigned_username'], '-- None --', g.user['user_id'], g.user['username'])
    )
    db.execute(
        "UPDATE tickets SET assigned_user_id = ?, assigned_username = ? WHERE ticket_id = ?", ("", "-- None --", ticket_id)
    )
    db.commit()
    flash('ticket unassigned')


    return redirect(url_for('teams.manageUser', user_id=user_id))


@bp.route('/ticket/<int:ticket_id>/user/<int:user_id>/assign')
@login_required
@s3_required
def assignTicket(ticket_id, user_id):
    user = get_user(user_id)
    db = get_db()
    ticket = get_ticket(ticket_id)
    db.execute(
        "INSERT INTO ticket_changelog (ticket_id, property, old_value, new_value, author_id, author_username) VALUES (?, ?, ?, ?, ?, ?)", (ticket_id, 'assigned_username', ticket['assigned_username'], user['username'], g.user['user_id'], g.user['username'])
    )
    db.execute(
        "UPDATE tickets SET assigned_user_id = ?, assigned_username = ? WHERE ticket_id = ?", (user_id, user['username'], ticket_id)
    )
    db.commit()
    flash('ticket assigned')


    return redirect(url_for('teams.manageUser', user_id=user_id))