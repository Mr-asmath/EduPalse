from flask import Flask, g
from flask_login import LoginManager
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

login_manager = LoginManager()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '8152910e735aacdce1f3e1707c69b49e290c726c8a06bfde00cfec5419f5f683'

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .routes import main
    app.register_blueprint(main)

    app.teardown_appcontext(close_db)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    return app
