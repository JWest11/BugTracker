import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_user(user_id):
    user = get_db().execute(
        "SELECT username, user_id, security_level FROM users WHERE user_id == ?", (user_id,)
    ).fetchone()

    return user

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/register', methods=('GET', 'POST'))
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            error = 'usernaame and password required'

        if not error:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"Username: {username} is already taken."
                flash(error)
            else:
                flash("Successfully registered!")
                return redirect(url_for("auth.login"))
    
    return render_template('auth/register.html', error = error)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if not user or not check_password_hash(user['password'], password):
            error = "Invalid credentials"
            flash(error)
        
        if not error:
            session.clear()
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            flash(f"logged in as {username}")
            return redirect(url_for('dashboard.index'))
    
    return render_template('auth/login.html')

@bp.route('/demoLogin', methods=('GET', 'POST'))
def demoLogin():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if not user or not check_password_hash(user['password'], password):
            error = "Invalid credentials"
            flash(error)
        
        if not error:
            session.clear()
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            flash(f"logged in as {username}")
            return redirect(url_for('dashboard.index'))
    
    return render_template('auth/demoLogin.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged Out')
    return redirect(url_for('auth.login'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE user_id = ?', (user_id,)
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

def s2_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['security_level'] < 2:
            return redirect(url_for('dashboard.index'))
        
        return view(**kwargs)
    
    return wrapped_view

def s3_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['security_level'] < 3:
            return redirect(url_for('dashboard.index'))
        
        return view(**kwargs)
    
    return wrapped_view