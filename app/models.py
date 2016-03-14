# -*- coding: utf-8 -*-

'''
 基本模型类
'''
from app import db
from . import login_manager
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class Developer(db.Model):

    """
    开发者模型类
    tablename tb_developer
    """

    __tablename__ = 'tb_developer'

    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    username = db.Column(db.String(20), default='')
    # 密码
    password = db.Column(db.String(20), default='')
    # 昵称
    nickname = db.Column(db.String(20), default='')
    # 是否确认
    confirmed = db.Column(db.Boolean, default=False)
    # 性别
    sex = db.Column(db.Integer, default=1)
    # qq账号
    qq = db.Column(db.String(60), default='')
    # 微博账号
    weibo = db.Column(db.String(60), default='')
    # Github账号
    github = db.Column(db.String(200), default='')
    # 学校
    school = db.Column(db.String(30), default='')
    # 邮箱
    email = db.Column(db.String(60), default='')
    # 电话号码
    phone = db.Column(db.String(20), default='')
    # 爱好
    hobby = db.Column(db.String(200), default='')
    # 自我介绍
    info = db.Column(db.String(200), default='')
    # 学位
    degree = db.Column(db.String(10), default='')
    # 注册时间
    register_time = db.Column(db.DateTime, default=datetime.now())
    # 关联的app列表
    apps = db.relationship('App', backref='developer', lazy='dynamic')

    def __init__(self, **kwargs):
        """
        初始化函数
        """
        super(Developer, self).__init__(**kwargs)


    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm' : self.id})


    def confirm(self, token):
        """
        身份验证
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    def verify_password(self, password):
        """
        确认密码是否正确
        """
        if self.password == password:
            return True
        else:
            return False


    def save(self):
        """
        保存用户数据模型数据
        """
        db.session.add(self)
        db.session.commit()


    def update(self, info):
        """
        更新用户数据
        info 更新的数据集 Dict
        """
        db.session.query(Developer).\
            filter_by(username=self.username).update(info)
        db.session.commit()


    def to_json(self):
        """
        将数据转化为json格式
        """
        json_post = dict(username=self.username, nickname=self.nickname,
                         sex=self.sex, qq=self.qq, weibo=self.weibo, github=self.github,
                         school=self.school, phone=self.phone, hobby=self.hobby, info=self.info)
        return json_post


# App类
class App(db.Model):

    """
    App数据模型
    tablename tb_app
    """

    __tablename__ = 'tb_app'

    id = db.Column(db.Integer, primary_key=True)

    # app 名称
    app_name = db.Column(db.String(20), unique=True)
    # app Key
    app_key = db.Column(db.String(20), default="")
    # app 介绍
    description = db.Column(db.String(200), default='')
    # app 当前状态
    status = db.Column(db.Integer, default=0)
    # app 应用场景
    platform = db.Column(db.Integer, default=-1)
    # app创建时间
    create_time = db.Column(db.DateTime, default=datetime.now())
    # 对应的开发者ID
    developer_id = db.Column(db.Integer, db.ForeignKey('tb_developer.id'))


    def __init__(self, **kwargs):
        """
        初始化函数
        """
        super(App, self).__init__(**kwargs)


    def save(self):
        """
        保存对象
        """
        self.create_time = datetime.now()
        # 默认设置为未审核
        self.status = 0

        db.session.add(self)
        db.session.commit()


    def find(self, content):
        """
        按照搜索内容进行搜索
        """
        return db.session.query(content).filter(App.app_name.like(content)).\
            order_by(self.create_time.desc).all()


    def to_json(self):
        """
        将数据转化为json格式
        """
        json_post = dict(app_name=self.app_name, description=self.description,
                         status=self.status, create_time=self.create_time)
        return json_post


