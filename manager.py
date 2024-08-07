from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Admin, User, add_admin, add_user

manager_blueprint = Blueprint('manager', __name__)


@manager_blueprint.route('/user_manager',methods=['GET', 'POST'])
@login_required
def user_manager():
    try:
        page = int(request.args['page'])
    except:
        page = 1
    
    users = User.query.paginate(page=page,per_page=20,error_out=False)

    next_url = url_for('manager.user_manager', page=users.next_num) if users.has_next else None
    prev_url = url_for('manager.user_manager', page=users.prev_num) if users.has_prev else None

    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['lastname']
        nfc_id = request.form['ID']

        if name and last_name and nfc_id:
            if User.query.filter_by(nfc_id=nfc_id).first():
                return render_template('user_manager.html', users=users, cant_register=True)
            add_user(name, last_name, nfc_id)
            return render_template('user_manager.html', users=users, register=True)

    return render_template('user_manager.html', users=users)

@manager_blueprint.route("/admin_manager",methods=['GET','POST'])
@login_required
def admin_manager():
    try:
        page = int(request.args['page'])
    except:
        page = 1
    
    admins = Admin.query.with_entities(Admin.admin_name, Admin.admin_last_name, Admin.email, Admin.id).paginate(page=page,per_page=20,error_out=False)

    next_url = url_for('manager.admin_manager', page=admins.next_num) if admins.has_next else None
    prev_url = url_for('manager.admin_manager', page=admins.prev_num) if admins.has_prev else None

    if request.method == 'POST':
        admin_name = request.form['name']
        admin_last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        if admin_name and admin_last_name and email and password:
            if Admin.query.filter_by(email=email).first():
                return render_template('admin_manager.html', admins=admins, cant_register=True)
            add_admin(admin_name, admin_last_name, email, password)
            return render_template('admin_manager.html', admins=admins, register=True)

    return render_template('admin_manager.html', admins=admins)