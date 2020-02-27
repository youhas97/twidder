# Flask shit
from flask import Flask, Response, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)

# Other shit
from werkzeug.security import generate_password_hash, check_password_hash
from server import db, jwt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)

    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)

    def empty_fields(self):
        if (self.email == "" or self.password == "" or self.firstname == ""
        or self.lastname == "" or self.gender == "" or self.city == ""
        or self.country == ""):
            return True
        else:
            return False

    def pw_correct_len(self):
        return len(self.password) >= 8


# Sign in
def sign_in(email, pw):
    user = User.query.filter_by(email=email).first()
    if (user is None):
        return jsonify({"message": "Incorrect email adress."}), 401
    elif (check_password_hash(user.password, pw)):
        resp = make_response({"message": "Sucessfully signed in."}, 200)
        resp.headers['Authorization'] = "Bearer " + create_access_token(identity=email)
        return resp
    else:
        return jsonify({"message": "Incorrect password."}), 401


# Sign up
def sign_up(email, pw, fname, lname, gender, city, country):
    hashed_pw = generate_password_hash(pw)
    user = User(email=email, password=hashed_pw, firstname=fname,
    lastname=lname, gender=gender, city=city, country=country)

    if (User.query.filter_by(email=email).first() is None):
        if (not user.empty_fields()):
            if (user.pw_correct_len()):
                db.session.add(user)
                db.session.commit()
            else:
                return jsonify({"message": "Password must be at least 8 characterts long."}), 401
        else:
            return jsonify({"message": "Please fill out all forms."}), 401
    else:
        return jsonify({"message": "User already exists."}), 401

    resp = make_response()

    return jsonify({"message": "User created."}), 200

# Sign out
def sign_out():
    return 'test'

# Change password
def change_password():
    return 'test'

# Get user data by token
def get_user_data_by_token():
    return 'test'

# Get user data by email
def get_user_data_by_email():
    return 'test'

# Get user messages by token
def get_user_messages_by_token():
    return 'test'

# Get user messages by email
def get_user_messages_by_email():
    return 'test'

# Post messages to wall
def post_message():
    return 'test'