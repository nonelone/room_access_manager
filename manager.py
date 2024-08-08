from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Admin, User, Tokens, Lock, add_admin, add_user, connect_lock, disconnect_lock

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


@manager_blueprint.route("/access_manager",methods=['GET','POST'])
@login_required
def access_manager():
    if request.method == 'POST':
        user_id = request.form['user_id']
        lock_to_connect = None
        try:
            
            lock_to_connect = request.form['lock_id']
            deleting = request.form['to_delete']
            print(deleting)
            if lock_to_connect != None and user_id != '':
                if deleting == 'True':
                    disconnect_lock(lock_to_connect, user_id)
                else:
                    connect_lock(lock_to_connect, user_id)

        except: print("Opening page")
        
        connected_locks = db.session.query(Lock).join(Tokens, Lock.id == Tokens.lock_id, isouter=True).filter(Tokens.nfc_id == user_id).all()#
        Tokens.query.filter_by(nfc_id=user_id).all()
        locks_ids = []
        for lock in connected_locks: locks_ids.append(lock.id)
        avaliable_locks = Lock.query.filter(Lock.id.not_in(locks_ids)).all()
         #db.session.query(Lock).join(Tokens, Lock.id == Tokens.lock_id, isouter=True).filter(Tokens.nfc_id == None).all()
        user = User.query.filter_by(nfc_id=user_id).first()
        return render_template('access_manager.html', user=user, connected_locks=connected_locks, avaliable_locks=avaliable_locks)

    return render_template('404.html')