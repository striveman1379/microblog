# -*- coding:utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #用于在前端表单那里生成用于保护表单免受CSRF攻击的token
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    #指定舒勇数据库的连接地址
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir,'app.db')

    #关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False


