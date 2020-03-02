from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from server import db

db.drop_all()
db.create_all()
