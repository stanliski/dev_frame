from flask import render_template, redirect, url_for

def unlogin(message):
    return redirect(url_for('main.index'))