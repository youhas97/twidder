import functools
from flask import Flask, request, jsonify, make_response, render_template, escape
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send, disconnect, join_room
from flask_login import LoginManager, login_required, logout_user, current_user
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)

secret_key = '4cebdc598eef4ba935c8ea889af0afb30e8505f7005186c484d7ac506d8c7ac8'
UPLOAD_FOLDER = '/static/assets/img'

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = secret_key
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)

import database_helper as helper

blacklist = set()

# Method will be called whenever the specified tokens
# are used to access a protected endpoint
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@login_manager.user_loader
def load_user(user_id):
    return helper.load_user(user_id)

@app.route('/', methods = ["GET"])
def client():
    return render_template('client.html')

# Sign in
@app.route('/sign_in', methods = ['POST'])
def sign_in():
    email = escape(request.json['email'])
    pw = escape(request.json['password'])

    return helper.sign_in(email, pw)

# Sign up
@app.route('/sign_up', methods = ['POST'])
def sign_up():
    if request.method == 'POST':
        email = escape(request.json['email'])
        pw = escape(request.json['password'])
        fname = escape(request.json['firstname'])
        lname = escape(request.json['familyname'])
        gender = escape(request.json['gender'])
        city = escape(request.json['city'])
        country = escape(request.json['country'])

        return helper.sign_up(email, pw, fname, lname, gender, city, country)

# Sign out
@app.route('/sign_out', methods = ['POST'])
@jwt_required
@login_required
def sign_out():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    logout_user()
    return make_response({"msg": "Successfully signed out."}, 200)

# Change password
@app.route('/change_password', methods = ['POST'])
@jwt_required
def change_password():
    email = get_jwt_identity()
    old_pw = escape(request.json['oldPassword'])
    new_pw = escape(request.json['newPassword'])
    return helper.change_password(email, old_pw, new_pw)

# Get user data by token
@app.route('/get_user_data_by_token', methods = ['POST'])
@jwt_required
def get_user_data_by_token():
    email = get_jwt_identity()
    return helper.get_user_data(email)

# Get user data by email
@app.route('/get_user_data_by_email', methods = ['POST'])
@jwt_required
def get_user_data_by_email():
    email = escape(request.json['email'])
    return helper.get_user_data(email)

# Get user messages by token
@app.route('/get_user_messages_by_token', methods = ['POST'])
@jwt_required
def get_user_messages_by_token():
    email = get_jwt_identity()
    return helper.get_user_messages(email)

# Get user messages by email
@app.route('/get_user_messages_by_email', methods = ['POST'])
@jwt_required
def get_user_messages_by_email():
    email = escape(request.json['email'])
    return helper.get_user_messages(email)

# Post messages to wall
@app.route('/post_message', methods = ['POST'])
@jwt_required
def post_message():
    writer = get_jwt_identity()
    recipient = escape(request.json['email'])
    message = escape(request.json['message'])
    return helper.post_message(writer, recipient, message)

@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)

@socketio.on('disconnect')
def disconnection():
    print('Websocket disconnected')

@socketio.on('connect')
def connect_handler():
    if current_user.is_authenticated:
            emit('forced-dc', {'message': 'Someone else has logged in with the same account'},
            room=current_user.email)
            join_room(current_user.email)
    else:
        return False

if __name__ == '__main__':
    socketio.run(app)