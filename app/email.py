from flask.ext.mail import Message
from flask import current_app, render_template
from flask.ext.mail import Mail
from threading import Thread

mail = Mail(current_app)

current_app.config['MAIL_SUBJECT_PREFIX'] = '[Flasky]'
current_app.config['MAIL_SENDER'] = 'Flasky Admin'


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[current_app, msg])
    thr.start()
    return thr