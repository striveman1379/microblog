# -*- coding:utf-8 -*-
from app import app, db

from flask_script import Manager
from app.models import User, Post


#pp.shell_context_processor装饰器将该函数注册为一个shell上下文函数。
# 当flask shell命令运行时，它会调用这个函数并在shell会话中注册它返回的项目。
# 函数返回一个字典而不是一个列表，原因是对于每个项目，你必须通过字典的键提供一个名称以便在shell中被调用。
@app.shell_context_processor
def make_shell_context():
    return {'db': db, "User": User, 'Post': Post}


manager = Manager(app)


if __name__ == '__main__':

    manager.run()
