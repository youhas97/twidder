from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
        lname = request.args['lastname']
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
    return jsonify({"message": "Successfully signed out."}), 200

# Change password
@app.route('/function/change_password')
def change_password():
    return 'test'

# Get user data by token
@app.route('/function/get_user_data_by_token')
def get_user_data_by_token():
    return 'test'

# Get user data by email
@app.route('/function/get_user_data_by_email')
def get_user_data_by_email():
    return 'test'

# Get user messages by token
@app.route('/function/get_user_messages_by_token')
def get_user_messages_by_token():
    return 'test'

# Get user messages by email
@app.route('/function/get_user_messages_by_email')
def get_user_messages_by_email():
    return 'test'

# Post messages to wall
@app.route('/function/post_message')
def post_message():
    return 'test'

