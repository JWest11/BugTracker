from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flaskr.db import get_db
from flaskr.auth import get_user, login_required, s2_required, s3_required
from flaskr.projects import get_project, get_project_users, get_all_projects, get_project_tickets
from flaskr.tickets import get_user_tickets

bp = Blueprint('account', __name__)

@bp.route('/account')
@login_required
def account():
    return render_template('account.html', g = g)