import os
from flask import Flask

def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY= 'DEV',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads'),
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'},
        MAX_CONTENT_LENGTH = 16 * 1000 * 1000,
    )

    try:
        os.makedirs(app.instance_path)
    except:
        pass

    try:
        uploadPath = os.path.join(app.instance_path, 'uploads')
        os.makedirs(uploadPath)
    except:
        pass


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import projects
    app.register_blueprint(projects.bp)

    from . import tickets
    app.register_blueprint(tickets.bp)

    from . import teams
    app.register_blueprint(teams.bp)

    from . import files
    app.register_blueprint(files.bp)

    from . import dashboard
    app.register_blueprint(dashboard.bp)

    from . import account
    app.register_blueprint(account.bp)

    
    
    return app