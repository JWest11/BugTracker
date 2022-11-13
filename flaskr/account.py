from flask import Blueprint, g, render_template
from flaskr.auth import login_required

bp = Blueprint('account', __name__)

@bp.route('/account')
@login_required
def account():
    return render_template('account.html', g = g)