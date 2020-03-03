from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)

# Used to generate secret key
import secrets

secret_key = secrets.token_hex()

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = secret_key
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
db = SQLAlchemy(app)
jwt = JWTManager(app)

import database_helper as helper

blacklist = set()

# Method will be called whenever the specified tokens
# are used to access a protected endpoint
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@app.route('/', methods = ["GET"])
@jwt_required
def protected():
    return 'Hello, World!'

# Sign in
@app.route('/function/sign_in', methods = ['POST'])
def sign_in():
    email = request.args['email']
    pw = request.args['password']

    return helper.sign_in(email, pw)

# Sign up
@app.route('/function/sign_up', methods = ['POST'])
def sign_up():
    if request.method == 'POST':
        email = request.args['email']
        pw = request.args['password']
        fname = request.args['firstname']
        lname = request.args['familyname']
        gender = request.args['gender']
        city = request.args['city']
        country = request.args['country']

        return helper.sign_up(email, pw, fname, lname, gender, city, country)



# Sign out
@app.route('/function/sign_out', methods = ['DELETE'])
@jwt_required
def sign_out():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    resp = make_response({"message": "Successfully signed out."}, 200)
    return resp

# Change password
@app.route('/function/change_password', methods = ['POST'])
@jwt_required
def change_password():
    email = get_jwt_identity()
    old_pw = request.args['oldPassword']
    new_pw = request.args['newPassword']
    return helper.change_password(email, old_pw, new_pw)

# Get user data by token
@app.route('/function/get_user_data_by_token', methods = ['POST'])
@jwt_required
def get_user_data_by_token():
    email = get_jwt_identity()
    return helper.get_user_data(email)

# Get user data by email
@app.route('/function/get_user_data_by_email', methods = ['POST'])
@jwt_required
def get_user_data_by_email():
    email = request.args['email']
    return helper.get_user_data(email)

# Get user messages by token
@app.route('/function/get_user_messages_by_token', methods = ['POST'])
@jwt_required
def get_user_messages_by_token():
    email = get_jwt_identity()
    return helper.get_user_messages(email)

# Get user messages by email
@app.route('/function/get_user_messages_by_email', methods = ['POST'])
@jwt_required
def get_user_messages_by_email():
    email = request.args['email']
    return helper.get_user_messages(email)

# Post messages to wall
@app.route('/function/post_message', methods = ['POST'])
@jwt_required
def post_message():
    writer = get_jwt_identity()
    recipient = request.args['email']
    message = request.args['message']
    return helper.post_message(writer, recipient, message)

