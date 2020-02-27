from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import database_helper as helper

@app.route('/')
def hello_world():
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
@app.route('/function/sign_out')
def sign_out():
    return 'test'

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

