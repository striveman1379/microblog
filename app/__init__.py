# -*- coding:utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)

#指定login视图函数用于处理登录认证
#‘login’值是登录视图函数（endpoint）名，换句话说该名称可用于url_for()函数的参数并返回对应的URL
login.login_view = 'login'

#不在顶部导入是为了解决循环导入问题
from app import routes,models

