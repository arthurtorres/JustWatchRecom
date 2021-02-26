# init.py
from .commands import create_tables
from .extensions import db, login_manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 




def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)


    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Usuario.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    app.cli.add_command(create_tables)
    return app





