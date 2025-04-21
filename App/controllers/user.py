from App.models import User
from App.database import db
from sqlalchemy.exc import SQLAlchemyError

def create_user(username, password):
    try:
        newuser = User(username=username, password=password)
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except SQLAlchemyError as e:
        print(f"Error creating user: {e}")
        db.session.rollback()
        return None


def get_user_by_username(username):
    try:
        return User.query.filter_by(username=username).first()
    except SQLAlchemyError as e:
        print(f"Error fetching user by username: {e}")
        return None


def get_user(id):
    try:
        return User.query.get(id)
    except SQLAlchemyError as e:
        print(f"Error fetching user by ID: {e}")
        return None


def get_all_users():
    try:
        return User.query.all()
    except SQLAlchemyError as e:
        print(f"Error fetching all users: {e}")
        return []


def get_all_users_json():
    try:
        users = User.query.all()
        if not users:
            return []
        return [user.get_json() for user in users]
    except SQLAlchemyError as e:
        print(f"Error fetching users in JSON: {e}")
        return []


def update_user(id, username):
    try:
        user = get_user(id)
        if user:
            user.username = username
            db.session.add(user)
            db.session.commit()
            return user
        else:
            print(f"No user found with ID {id}")
            return None
    except SQLAlchemyError as e:
        print(f"Error updating user: {e}")
        db.session.rollback()
        return None