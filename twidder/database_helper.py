# Flask shit
from flask import Flask, Response, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)

# Other shit
from werkzeug.security import generate_password_hash, check_password_hash
from server import db, jwt
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    firstname = db.Column(db.String, nullable=False)
    familyname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)

    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)

    messages = db.Column(db.String, nullable=False)

    current_socket = None

    def empty_fields(self):
        if (self.email == "" or self.password == "" or self.firstname == ""
        or self.familyname == "" or self.gender == "" or self.city == ""
        or self.country == ""):
            return True
        else:
            return False

# Sign in
def sign_in(email, pw):
    user = User.query.filter_by(email=email).first()
    if (user is None):
        return make_response({"msg": "Incorrect email adress."}, 400)
    elif (check_password_hash(user.password, pw)):
        resp = make_response({"msg": "Sucessfully signed in."}, 200)
        resp.headers['Authorization'] = "Bearer " + create_access_token(identity=email)
        login_user(user)
        return resp
    else:
        return make_response({"msg": "Incorrect password."}, 400)

# Sign up
def sign_up(email, pw, fname, lname, gender, city, country):
    hashed_pw = generate_password_hash(pw)
    if (len(pw) < 8):
        return make_response({"msg": "Password must be at least 8 characterts long."}, 400)

    user = User(email=email, password=hashed_pw, firstname=fname,
    familyname=lname, gender=gender, city=city, country=country, messages="[]")

    if (User.query.filter_by(email=email).first() is None):
        if (not user.empty_fields()):
            db.session.add(user)
            db.session.commit()
        else:
            return make_response({"msg": "Please fill out all forms."}, 400)
    else:
        return make_response({"msg": "Email already in use."}, 400)

    return make_response({"msg": "User created successfully."}, 200)


# Change password
def change_password(email, old_pw, new_pw):
    hashed_new_pw = generate_password_hash(new_pw)

    user = User.query.filter_by(email=email).first()

    if (not check_password_hash(user.password, old_pw)):
        return make_response({"msg": "Incorrect old password."}, 400)
    elif (len(new_pw) < 8):
        return make_response({"msg": "Password must be at least 8 characters long."}, 400)
    else:
        user.password = hashed_new_pw
        db.session.commit()
        return make_response({"msg": "Password changed successfully."}, 200)

# Get user data
def get_user_data(email):
    user = User.query.filter_by(email=email).first()
    if (user is None):
        return make_response({"msg": "No such user."}, 400)
    else:
        result = {
            "email": user.email,
            "firstname": user.firstname,
            "familyname": user.familyname,
            "gender": user.gender,
            "city": user.city,
            "country": user.country
        }
        return make_response(result, 200)

# Get user messages
def get_user_messages(email):
    user = User.query.filter_by(email=email).first()

    if (user is None):
        return make_response({"msg": "No such user."}, 400)
    else:
        return make_response(user.messages, 200)

# Post messages to wall
def post_message(writer, recipient, message):
    user = User.query.filter_by(email=recipient).first()

    if (user is None):
        return make_response({"msg": "No such user."}, 400)
    else:
        message = {
            "writer": writer,
            "message": message
        }
        messages = json.loads(user.messages)
        messages.insert(0, message)
        user.messages = json.dumps(messages)
        db.session.commit()

        return make_response({"msg": "Message successfully posted."}, 200)

def load_user(user_id):
    return User.query.get(int(user_id))