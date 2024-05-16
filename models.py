from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

import os.path
import getpass

db = SQLAlchemy()


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    email = db.Column(db.String(191), nullable=False)
    admin_name = db.Column(db.String(30), nullable=False)
    admin_last_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String, nullable=False)

class Nfc_id(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    owner_name = db.Column(db.String(30), nullable=False)
    owner_last_name = db.Column(db.String(30), nullable=False)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    token_name = db.Column(db.String(30), nullable=False, unique=True)

class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nfc_id = db.Column(db.Integer, db.ForeignKey(Nfc_id.id))
    token_id = db.Column(db.Integer, db.ForeignKey(Token.id))

def add_admin(name, last_name, email, password):
    print('Creating new admin account...')
    if Admin.query.filter_by(email=email).first() is None:
        new_admin = Admin(admin_name=name, admin_last_name = last_name, email=email, password=generate_password_hash(password))
        db.session.add(new_admin)
        db.session.commit()


def init_database():
    if os.path.isfile('instance/db'):
        print("Found database...")
    else:
        print("Database not found! Creating new database...")
        db.create_all()

    if Admin.query.first() is not None:
        pass
    else:
        print("No admin has been found!\nYou need to create admin!")
        name = input("Admin's name: ")
        last_name = input("Admin's last name: ")
        email = input("Admin's email: ")
        password = getpass.getpass(prompt="Admin's password: ") #Password will not be echoed
        if name and last_name and email and password:
            add_admin(name, last_name, email, password)

    print("Database initialized...")