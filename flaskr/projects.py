from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flaskr.auth import login_required, s2_required, s3_required
from flaskr.db import get_db


bp = Blueprint('projects', __name__)


def get_project(id):
    project = get_db().execute(
        "SELECT * FROM projects WHERE project_id == ?", (id,)
    ).fetchone()

    return project

def get_project_users(project_id):
    db = get_db()
    project_users_ids = db.execute(
        "SELECT * FROM users_projects WHERE project_id = ?", (project_id,)
    ).fetchall()

    project_users = []
    for row in project_users_ids:
        project_users.append(
            db.execute(
                "SELECT username, user_id, security_level FROM users WHERE user_id = ?", (row['user_id'],)
            ).fetchone()
        )
    return project_users

def get_all_projects():
    projects = get_db().execute(
        "SELECT * FROM projects"
    ).fetchall()

    return projects

def get_project_tickets(project_id):
    tickets = get_db().execute(
        "SELECT * FROM tickets WHERE project_id == ?", (project_id,)
    ).fetchall()

    return tickets


@bp.route('/projects/all')
@login_required
@s2_required
def allProjects():

    from flaskr.teams import get_users_projects

    projects = None
    if g.user['security_level'] < 3:
        projects = get_users_projects(g.user['user_id'])
    else:
        projects = get_all_projects()
        

    return render_template('projects/projects.html', g = g, projects = projects, projectCount = len(projects))

@bp.route('/projects/my')
@login_required
def myProjects():
    db = get_db()
    usersProjects = db.execute(
        "SELECT * FROM users_projects WHERE user_id == ?", (g.user['user_id'],)
    ).fetchall()
    projects = []
    for p in usersProjects:
        projects.append(db.execute(
            "SELECT * FROM projects WHERE project_id == ?", (p['project_id'],)
        ).fetchone())


    return render_template('projects/projects.html', g = g, projects = projects)


@bp.route('/projects/create', methods=('GET', 'POST'))
@login_required
@s3_required
def createProject():
    error = None

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        if not title or not description:
            error = 'title and description required'
            flash(error)
        
        if not error:
            db = get_db()
            db.execute(
                "INSERT INTO projects (title, description) VALUES (?, ?)", (title, description)
            )
            db.commit()
            flash('project created')
            return redirect(url_for('projects.allProjects'))
    

    return render_template('projects/createProject.html', g = g)


@bp.route('/projects/<int:project_id>/view')
@login_required
@s2_required
def viewProject(project_id):
    project = get_project(project_id)
    project_users = get_project_users(project_id)
    db = get_db()
    tickets = get_project_tickets(project_id)
    chartData = [0,0,0,0]
    mapping = {"High":0, "Medium":1, "Low":2}
    for ticket in tickets:
        chartData[mapping[ticket['priority']]] +=1
    if len(tickets) == 0:
        chartData = [0,0,0,1]
    

    return render_template('projects/viewProject.html', project = project, tickets = tickets, ticketCount = len(tickets), project_users = project_users, memberCount = len(project_users), donutData = str(chartData))


@bp.route('/projects/<int:project_id>/update', methods=('GET', 'POST'))
@login_required
@s3_required
def updateProject(project_id):
    error = None

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        if not title or not description:
            error = 'title and description required'
            flash(error)
        
        if not error:
            db = get_db()
            db.execute(
                "UPDATE projects SET title = ?, description = ? WHERE project_id = ?", (title, description, project_id)
            )
            db.commit()
            flash('project updated')
            return redirect(url_for('projects.allProjects'))
    
    
    project = get_project(project_id)

    return render_template('projects/updateProject.html', project = project)

@bp.route('/projects/<int:project_id>/delete', methods=('GET', 'POST'))
@login_required
@s3_required
def deleteProject(project_id):
    db = get_db()
    db.execute(
        "DELETE FROM projects WHERE project_id = ?", (project_id,)
    )
    db.execute(
        "DELETE FROM users_projects WHERE project_id = ?", (project_id,)
    )
    db.commit()
    flash('project deleted')

    return redirect(url_for('projects.allProjects'))