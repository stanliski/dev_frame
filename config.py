# -*- coding: utf-8 -*-

'''
项目基本配置类,包括MySQL数据库的连接密码,端口
定义了两套基本配置环境,即开发环境和测试环境
'''

class Config:
    DEBUG = False
    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123@127.0.0.1:3306/indoor'
    SECRET_KEY = 'DEVELOPER'
    APP_LIST_PER_PAGE = 10
    @staticmethod
    def init_app(app):
        pass

# 开发环境
class DevelopingConfig(Config):

    DEBUG = True


# 测试环境
class TestingConfig(Config):
    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
    DEBUG = True


config = {
    'developer':    DevelopingConfig,
    'test':         TestingConfig,
    'default':      DevelopingConfig
}