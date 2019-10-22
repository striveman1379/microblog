# -*- coding:utf-8 -*-
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index = True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    '''
    db.relationship字段通常在“一”的这边定义，并用作访问“多”的快捷方式
    因此，我有一个用户实例u，表达式u.posts将运行一个数据库查询，返回该用户发表过的所有动态
    参数"Post"为多，backref参数定义了代表“多”的类的实例反向调用“一”的时候的属性名称。这将会为用户动态添加一个属性post.author,
    调用它将返回给用户动态的用户实例
    lazy参数东一了这种关系调用的数据库查询是如何执行的
    '''
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    #该类的__repr__方法用于在调试时打印用户实例。
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DATETIME,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)