#! /usr/bin/env/ python

from flask.ext.script import Manager
from app import create_app
from app import db


app = create_app('test')
manager = Manager(app)


@manager.command
def run():
    app.run(host='0.0.0.0', port=5000, debug=True)


@manager.command
def create_db():
    db.drop_all()
    db.create_all()


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader.discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()