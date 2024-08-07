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
    try:
        page = int(request.args['page'])
    except:
        page = 1
    
    users = User.query.paginate(page=page,per_page=20,error_out=False)

    next_url = url_for('auth.manager', page=users.next_num) if users.has_next else None
    prev_url = url_for('auth.manager', page=users.prev_num) if users.has_prev else None

    admins = Admin.query.with_entities(Admin.admin_name, Admin.admin_last_name, Admin.email, Admin.id)

    return render_template('manager.html', users=users, admins=admins)

@auth_blueprint.route("/register",methods=['GET', 'POST'])
@login_required
def register():
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


@auth_blueprint.route("/manager",methods=['POST'])
@login_required
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['lastname']
        nfc_id = request.form['ID']

        if name and last_name and nfc_id:
            if User.query.filter_by(nfc_id=nfc_id).first():
                return render_template('manager.html', cant_register=True)
            add_user(name, last_name, nfc_id)
            return render_template('manager.html', register=True)

    return render_template('manager.html')

@auth_blueprint.route("/manager",methods=['POST'])
@login_required
def register_admin():
    if request.method == 'POST':
        admin_name = request.form['name']
        admin_last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        if admin_name and admin_last_name and email and password:
            if Admin.query.filter_by(email=email).first():
                return render_template('manager.html', cant_register=True)
            add_admin(admin_name, admin_last_name, email, password)
            return render_template('manager.html', register=True)

    return render_template('manager.html')