import sqlite3
import click
from flask import current_app, g
from werkzeug.security import generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db != None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode("utf8"))

def fill_db():
    db = get_db()

    hash = generate_password_hash("1234ABCD56")
    newUsers = [("Admin Demo", hash, 3), ("Manager Demo", hash, 2), ("Developer Demo", hash, 1), ("Kent", hash, 3), ("Jerry", hash, 2), ("Amy", hash, 2), ("Kate", hash, 2), ("Bob", hash, 1), ("Joe", hash, 1), ("John", hash, 1), ("Kim", hash, 1), ("Beck", hash, 1), ("Sally", hash, 1), ("Kamy", hash, 1), ("Cathy", hash, 1), ("Johnny", hash, 1)]

    for user in newUsers:
        db.execute(
            "INSERT INTO users (username, password, security_level) VALUES (?, ?, ?)", user
        )

    with current_app.open_resource('initialize.sql') as f:
        db.executescript(f.read().decode("utf8"))
        
    db.commit()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database initialized.')

@click.command('fill-db')
def fill_db_command():
    fill_db()
    click.echo('DB filled.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(fill_db_command)