# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, jsonify, request, current_app

from . import main
from app import db
from app.models import App, Developer
from ..email import send_email


# 开发者用户登陆
@main.route('/signin', methods=['GET', 'POST'])
def signin():

    if request.method == 'GET':
        return render_template('signin.html')

    email = request.form['email']
    password = request.form['password']

    if email.strip() == '' \
            or password.strip() == '':
        return jsonify({'status':401})

    if email.find("@") == -1:
        developer = Developer.query.filter_by(username=email).first()
    else:
        developer = Developer.query.filter_by(email=email).first()

    if developer is not None:
        if developer.verify_password(password):
            session['username'] = developer.username
            session['password'] = developer.password
            return jsonify({'status':200})
        else:
            return jsonify({'status':402})
    else:
        return jsonify({'status':403})


# 开发者用户注册
@main.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'GET':
        return render_template('signup.html')

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    repassword = request.form['repassword']

    # 错误码判断
    if username.strip() == '' or repassword.strip() == '' \
            or password.strip() == '' or email.strip() == '':
        return jsonify({'status':401})

    if repassword != password:
        return jsonify({'status':402})

    if Developer.query.filter_by(username=username).first() != None \
            or Developer.query.filter_by(email=email).first() != None:
        return jsonify({'status':403})

    developer = Developer(username=username, password=password, email=email)

    try:
        developer.save()
    except Exception, e:
        print e

    token = developer.generate_confirmation_token()

    send_email(developer.email, 'Confirm Your Account', 'auth/email/confirm',
               developer=developer, token=token)
    # send_mail(developer.email, 'Confirm Your Account', '/email/confirm', developer=developer, token=token)

    return jsonify({'status' : 200})


# 开发者登出
@main.route('/logout')
def logout():
    session['username'] = None
    session['password'] = None
    return render_template('signin.html')


# 获取用户创建的APP列表
@main.route('/app/list', methods=['GET'])
def apps():

    if check_user_login():
        return redirect(url_for('main.signin'))

    # 数据进行分页处理
    page = request.args.get('page', 1, type=int)

    developer = Developer.query.filter_by(username=session.get("username")).first()

    pagination = App.query.filter_by(developer_id=developer.id).order_by(App.create_time.desc()).paginate(page,
                            per_page=current_app.config['APP_LIST_PER_PAGE'], error_out=False)

    apps = pagination.items

    return render_template('app-list.html',
                           apps=apps, pagination=pagination, pageNum=pagination.pages)


# 用户创建APP
@main.route('/app/create', methods=['GET', 'POST'])
def new_app():

    if check_user_login():
        return redirect(url_for('main.signin'))

    if request.method == 'GET':
        return render_template('new-app.html')

    app_name = request.form['app_name']
    platform = request.form.get('app_usage', 1, type=int)
    description = request.form['description']
    company = request.form.get('company', '', type=str)

    print session.get('username')

    developer = Developer.query.filter_by(username=session.get("username")).first()

    if description.strip() == '' or app_name.strip() == '':
        return render_template('new-app.html', warning='')

    app = App(app_name=app_name, description=description,
              platform=platform, company=company)

    app.developer = developer

    try:
        app.save()
    except Exception, e:
        print e

    return jsonify({'status':200, 'app':app.to_json()})



@main.route('/app/search', methods=['GET'])
def search_app():
    search_content = request.args.get('content', '', type=str)
    page = request.args.get('page', 1, type=int)
    if search_content.strip() == '':
        return redirect(url_for('main.apps'))

    pagination = App.query.filter(App.app_name==search_content).order_by(App.create_time.desc())\
        .paginate(page, per_page=current_app.config['APP_LIST_PER_PAGE'], error_out=False)

    apps = pagination.items

    return render_template('search-list.html',
                           apps=apps, pagination=pagination, pageNum=pagination.pages)



# 编辑开发者信息
@main.route('/user/edit', methods=['GET', 'POST'])
def edit_user():

    if check_user_login():
        return redirect(url_for('main.signin'))

    if request.method == 'GET':
        developer = Developer.query.filter_by(username=session.get('username')).first()
        return render_template('edit-user.html', developer=developer)

    username = session.get('username')
    nickname = request.form.get('nickname', '', type=str)
    sex = request.form.get('sex', 1, type=int)
    school = request.form.get('school', '', type=str)
    degree = request.form.get('degree', '', type=str)
    qq = request.form.get('qq', '', type=str)
    weibo = request.form.get('weibo', '', type=str)
    github = request.form.get('github', '', type=str)
    info = request.form.get('info', '', type=str)
    hobby = request.form.get('hobby', '', type=str)
    updateDic = dict({'nickname':nickname,'sex':sex,
                      'school':school,'degree':degree,
                      'qq':qq,'weibo':weibo,'github':github,
                      'info':info, 'hobby':hobby})

    developer = Developer.query.filter_by(username=username).first()

    try:
        developer.update(updateDic)
    except Exception, e:
        print e
        return jsonify({'status':400})

    developer = Developer.query.filter_by(username=username).first()

    print "%s, %s, %s" % (developer.nickname, developer.info, developer.hobby)

    return jsonify({'status':200, 'developer':developer.to_json()})


# 开发者信息
@main.route('/user/info')
def user_info():

    if check_user_login():
        return redirect(url_for('main.signin'))

    developer = Developer.query.\
        filter_by(username=session.get('username')).first();

    print developer.username
    print developer.qq
    print developer.weibo
    print developer.github

    return render_template('info.html', developer=developer)


@main.route('/user/modify')
def modify_password():
    return render_template('modify-password.html')


@main.route('/user/find-password')
def find_password():
    return render_template('find-password.html')


@main.route('/index')
def index():
    return render_template('index.html')


def check_user_login():
    if session.get('username') == None:
        return True
    else:
        return False