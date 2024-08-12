from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.middleware.proxy_fix import ProxyFix

from models import db, init_database, Admin

import os

from auth import auth_blueprint
from api import api_blueprint
from manager import manager_blueprint

app = Flask(__name__, instance_relative_config=True)

app.register_blueprint(auth_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(manager_blueprint)

app.config.from_object('config') # "global" configuration from config.py
app.config.from_pyfile('secrets.py') # "secret" configurations in instance/secrets.py

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))

@login_manager.unauthorized_handler
def handle_needs_login():
    return redirect(url_for('auth.login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def home_page():
    if current_user.is_authenticated: 
        return redirect(url_for('manager.manager'))
    return render_template('login.html')

if __name__ == "__main__":
    print(
        r"""
     __      __   _                    _         ___    _   __  __   _ 
     \ \    / /__| |__ ___ _ __  ___  | |_ ___  | _ \  /_\ |  \/  | | |
      \ \/\/ / -_) / _/ _ \ '  \/ -_) |  _/ _ \ |   / / _ \| |\/| | |_|
       \_/\_/\___|_\__\___/_|_|_\___|  \__\___/ |_|_\/_/ \_\_|  |_| (_)
        """
    )
    print("Initializing database...")
    with app.app_context():
        init_database()
    print(f"Starting app @ {app.config['HOST']}:{app.config['PORT']} with debug set to {app.config['DEBUG']}...")
    if app.config['BEHIND_PROXY']:
        print("Running behind a proxy...")
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
