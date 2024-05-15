from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from auth import auth_blueprint
from api import api_blueprint
from models import db, init_database, Admin

import os

app = Flask(__name__)

app.register_blueprint(auth_blueprint)
app.register_blueprint(api_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db'

with open("secrets.txt", "r") as f:
    app.config['SECRET_KEY'] = f.readline()

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
    return render_template("home.html")

if __name__ == "__main__":
    with app.app_context():
        init_database()
    app.run(debug=True, host='0.0.0.0', port=2137)
