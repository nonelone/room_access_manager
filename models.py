from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

import secrets
import os.path
import getpass

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email = db.Column(db.String(191), nullable=False)
    admin_name = db.Column(db.String(30), nullable=False)
    admin_last_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String, nullable=False)

class User(db.Model):
    nfc_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_name = db.Column(db.String(30), nullable=False)
    user_last_name = db.Column(db.String(30), nullable=False)

class Lock(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    lock_name = db.Column(db.String(30), nullable=False, unique=True)
    token = db.Column(db.String(255), nullable=False, unique=True)

class Tokens(db.Model): #connections
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nfc_id = db.Column(db.Integer, db.ForeignKey(User.nfc_id))
    lock_id = db.Column(db.Integer, db.ForeignKey(Lock.id))

def add_admin(name, last_name, email, password):
    if Admin.query.filter_by(email=email).first() is None:
        new_admin = Admin(admin_name=name, admin_last_name = last_name, email=email, password=generate_password_hash(password))
        db.session.add(new_admin)
        db.session.commit()

def delete_admin(id):
    if int(id) != 1 and Admin.query.filter_by(id=id).first():
        db.session.query(Admin).filter(Admin.id==id).delete()
        db.session.commit()

def add_user(name, last_name, card_id):
    if User.query.filter_by(nfc_id=card_id).first() is None:
        new_user = User(user_name=name, user_last_name=last_name, nfc_id=card_id)
        db.session.add(new_user)
        db.session.commit()

def delete_user(nfc_id):
    if User.query.filter_by(nfc_id=nfc_id).first():
        db.session.query(User).filter(User.nfc_id==nfc_id).delete()
        db.session.query(Tokens).filter(Tokens.nfc_id==nfc_id).delete()
        db.session.commit()

def add_lock(lock_name):
    if Lock.query.filter_by(lock_name=lock_name).first() is None:
        token=secrets.token_hex(32)
        new_lock = Lock(lock_name=lock_name, token=token)
        db.session.add(new_lock)
        db.session.commit()
        return token

def connect_lock(lock_id,  nfc_id):
    if Tokens.query.filter_by(lock_id=lock_id).filter_by(nfc_id=nfc_id).first() is None:
        new_token = Tokens(nfc_id=nfc_id, lock_id=lock_id)
        db.session.add(new_token)
        db.session.commit()

def disconnect_lock(lock_id, nfc_id):
    _token = db.session.query(Tokens).filter(Tokens.lock_id==lock_id).filter(Tokens.nfc_id==nfc_id).first()
    if _token:
        db.session.query(Tokens).filter(Tokens.lock_id==lock_id).filter(Tokens.nfc_id==nfc_id).delete()
        db.session.commit()

def delete_lock(lock_id):
    if Lock.query.filter_by(id=lock_id).first():
        db.session.query(Lock).filter(Lock.id==lock_id).delete()
        db.session.query(Tokens).filter(Tokens.lock_id==lock_id).delete()
        db.session.commit()

def init_database():
    if os.path.isfile('instance/db'):
        print("Found database...")
    else:
        print("Database not found! Creating new database...")
        db.create_all()

    if Admin.query.first() is None:
        print("No admin has been found!\nYou need to create admin!")
        name = input("Admin's name: ")
        last_name = input("Admin's last name: ")
        email = input("Admin's email: ")
        password = getpass.getpass(prompt="Admin's password: ") #Password will not be echoed
        if name and last_name and email and password:
            add_admin(name, last_name, email, password)

    print("Database initialized...")