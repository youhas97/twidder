# Flask shit
from flask import Flask, Response, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)

# Other shit
from werkzeug.security import generate_password_hash, check_password_hash
from server import db, jwt
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    firstname = db.Column(db.String, nullable=False)
    familyname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)

    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)

    messages = db.Column(db.String, nullable=False)

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
        result = {
            "success": False,
            "message": "Incorrect email adress."
        }
        return make_response(result, 401)
    elif (check_password_hash(user.password, pw)):
        result = {
            "success": True,
            "message": "Sucessfully signed in."
        }
        resp = make_response(result, 200)
        resp.headers['Authorization'] = "Bearer " + create_access_token(identity=email)
        return resp
    else:
        result = {
                "success": False,
                "message": "Incorrect password."
            }
        return make_response(result, 401)


# Sign up
def sign_up(email, pw, fname, lname, gender, city, country):
    hashed_pw = generate_password_hash(pw)
    if (len(pw) < 8):
        result = {
                "success": False,
                "message":"Password must be at least 8 characterts long."
            }
        return make_response(result, 401)

    user = User(email=email, password=hashed_pw, firstname=fname,
    familyname=lname, gender=gender, city=city, country=country, messages="[]")

    if (User.query.filter_by(email=email).first() is None):
        if (not user.empty_fields()):
            db.session.add(user)
            db.session.commit()
        else:
            result = {
                "success": False,
                "message": "Please fill out all forms."
            }
            return make_response(result, 401)
    else:
        result = {
            "success": False,
            "message": "Email already in use."
        }
        return make_response(result, 401)

    result = {
            "success": True,
            "message": "User created successfully."
    }
    return make_response(result, 200)


# Change password
def change_password(email, old_pw, new_pw):
    hashed_new_pw = generate_password_hash(new_pw)

    user = User.query.filter_by(email=email).first()

    if (not check_password_hash(user.password, old_pw)):
        result = {
            "success": False,
            "message": "Incorrect old password."
        }
        return make_response(result, 401)
    elif (len(new_pw) < 8):
        result = {
            "success": False,
            "message": "Password must be at least 8 characters long."
        }
        return make_response(result, 401)
    else:
        user.password = hashed_new_pw
        db.session.commit()
        result = {
            "success": True,
            "message": "Password changed successfully."
        }
        return make_response(result, 200)

# Get user data
def get_user_data(email):
    user = User.query.filter_by(email=email).first()
    if (user is None):
        result = {
            "success": False,
            "message": "No such user."
        }
        return make_response(result, 401)
    else:
        result = {
            "success": True,
            "data" : {
                "email": user.email,
                "firstname": user.firstname,
                "familyname": user.familyname,
                "gender": user.gender,
                "city": user.city,
                "country": user.country
            }
        }
        return make_response(result, 200)

# Get user messages
def get_user_messages(email):
    user = User.query.filter_by(email=email).first()

    if (user is None):
        result = {
            "success": False,
            "message": "No such user."
        }
        return make_response(result, 401)
    else:
        result = {
            "success": True,
            "data": user.messages
        }
        return make_response(result, 200)

# Post messages to wall
def post_message(writer, recipient, message):
    user = User.query.filter_by(email=recipient).first()

    if (user is None):
        result = {
            "success": False,
            "message": "No such user."
        }
        return make_response(result, 401)
    else:
        message = {
            "writer": writer,
            "message": message
        }
        messages = json.loads(user.messages)
        messages.append(message)
        user.messages = json.dumps(messages)
        db.session.commit()

        result = {
            "success": True,
            "message": "Message successfully posted.",
        }
        return make_response(result, 200)