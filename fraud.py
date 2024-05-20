from faker import Faker
from models import add_admin, add_user, add_lock

from app import app
import models

fake = Faker()

def fake_admins(n):
    with app.app_context():
        for i in range(n):
            name = fake.name()
            add_admin(
                name.split(" ")[0], 
                name.split(" ")[1], 
                f"admin{i}@example.com", "admin"
            )

def fake_users(n):
    with app.app_context():
        for i in range(n):
            name = fake.name()
            add_user(
                name.split(" ")[0], 
                name.split(" ")[1], 
                int(i)
            )

def fake_locks(n):
    with app.app_context():
        for i in range(n):
            lock_name = f"Lock #{i}"
            _ = add_lock(lock_name)