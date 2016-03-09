from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask


test_app = Flask(__name__)

test_app.config.from_object('config.TestingConfig')

test_db = SQLAlchemy(test_app)