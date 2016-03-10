from flask import render_template, session, redirect, url_for, request
from . import auth
from errors import unlogin


# @auth.before_request
# def before_request():
#
#     if session.get('username') == None:
#         return unlogin('test')
#
#
# @auth.route('/regist')
# def regist():
#     return render_template('signing.html')

