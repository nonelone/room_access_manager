from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Admin, User, add_admin, add_user

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
            return redirect(url_for('manager.user_manager'))
        else: 
            print(f'Unauthorized login attempt by {request.remote_addr}')
            return render_template('login.html', bad=True)

    return render_template('login.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_blueprint.route("/register",methods=['GET', 'POST'])
@login_required
def old_register():
    if request.method == 'POST':
        name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']

        if name and last_name and email and password:
            if Admin.query.filter_by(email=email).first():
                return render_template('register.html', bad=True)
            add_admin(name, last_name, email, password)
            return render_template('register.html', good=True)
        else: 
            return render_template('register.html', bad=True)

    return render_template('register.html')