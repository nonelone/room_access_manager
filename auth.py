from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Admin

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('auth.manager'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        admin = Admin.query.filter_by(email=email).first()

        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('auth.manager'))
        else: 
            print(f'Unauthorized login attempt by {request.remote_addr}')
            return render_template('login.html', bad=True)

    return render_template('login.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/manager')
@login_required
def manager():
    return render_template('manager.html')

@auth_blueprint.route("/register")
@login_required
def register():
    return render_template('register.html')