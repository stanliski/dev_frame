# -*- coding: utf-8 -*-
'''
 基本模型类
'''
from app import db
from . import login_manager
from datetime import datetime


# 用户角色
class Role(db.Model):

    __tablename__ = 'tb_roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


# 基本用户类
class User(db.Model):

    __tablename__ = 'tb_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('tb_roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


# 开发者类
class Developer(db.Model):

    __tablename__ = 'tb_developer'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20))
    nickname = db.Column(db.String(20))
    sex = db.Column(db.Integer)
    qq = db.Column(db.String(60))
    weibo = db.Column(db.String(60))

    github = db.Column(db.String(200))
    password = db.Column(db.String(20))
    company = db.Column(db.String(30))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(60))
    description = db.Column(db.String(200))
    hobby = db.Column(db.String(200))
    register_time = db.Column(db.DateTime)

    apps = db.relationship('App', backref='developer', lazy='dynamic')


    def __init__(self, **kwargs):
        super(Developer, self).__init__(**kwargs)


    def verify_password(self, password):
        if self.password == password:
            return True
        else:
            return False


    def save(self):
        self.register_time = datetime.now()
        db.session.add(self)
        db.session.commit()


# App类
class App(db.Model):

    __tablename__ = 'tb_app'

    id = db.Column(db.Integer, primary_key=True)

    app_name = db.Column(db.String(20))
    company = db.Column(db.String(20))
    description = db.Column(db.String(200))
    status = db.Column(db.Integer)
    platform = db.Column(db.Integer)
    developer_id = db.Column(db.Integer, db.ForeignKey('tb_developer.id'))
    create_time = db.Column(db.DateTime)


    def __init__(self, **kwargs):
        super(App, self).__init__(**kwargs)


    # 保存APP对象
    def save(self):
        self.create_time = datetime.now()
        # 默认设置为未审核
        self.status = 0;

        db.session.add(self)
        db.session.commit()

    # 将数据转化为json格式
    def to_json(self):
        json_post = dict(app_name=self.app_name, description=self.description,
                         status=self.status, company=self.company, create_time=self.create_time)
        return json_post
