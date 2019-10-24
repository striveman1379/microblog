# -*- coding:utf-8 -*-
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index = True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(150))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)

    '''
    db.relationship字段通常在“一”的这边定义，并用作访问“多”的快捷方式
    因此，我有一个用户实例u，表达式u.posts将运行一个数据库查询，返回该用户发表过的所有动态
    参数"Post"为多，backref参数定义了代表“多”的类的实例反向调用“一”的时候的属性名称。这将会为用户动态添加一个属性post.author,
    调用它将返回给用户动态的用户实例
    lazy参数东一了这种关系调用的数据库查询是如何执行的
    '''
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    #设置密码-hash
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    #检查密码，返回值是True or False
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    #使用Flask-Login的@login.user_loader装饰器来为用户加载功能注册函数。
    # Flask-Login将字符串类型的参数id传入用户加载函数，因此使用数字ID的数据库需要如上所示地将字符串转换为整数。
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    '''
    User类新增的avatar()方法需要传入需求头像的像素大小，并返回用户头像图片的URL。 
    对于没有注册头像的用户，将生成“identicon”类的随机图片。 为了生成MD5哈希值，
    我首先将电子邮件转换为小写，因为这是Gravatar服务所要求的。 然后，因为Python中的MD5的参数类型需要是字节而不是字符串，
    所以在将字符串传递给该函数之前，需要将字符串编码为字节。
    '''
    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

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



