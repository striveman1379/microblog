# -*- coding:utf-8 -*-
from flask import render_template,flash,redirect,url_for
from flask import request
from app import app
from app import db
from app.forms import LoginForm,RegistrationForm
from flask_login import current_user,login_user,logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from app.models import User
from app.forms import EditProfileForm
from datetime import datetime

import logging
from logging import FileHandler


@app.route("/")
@app.route('/index')
@login_required        #用来拒绝匿名用户的访问，以保护某个视图函数
def index():
    posts = [
        {
            'author':{'username':"John"},
            'body':'Beautiful day in Portland!'
        },
        {
            'author': {'username': "Susan"},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template("index.html",title='Home Page',posts=posts)

#用户登录
@app.route("/login",methods=['GET','POST'])
def login():
    #is_authenticated检查用户书否登录，如果当前用户已登录，则重定向到主页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # print(current_user.is_authenticated)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for("login"))
        login_user(user,remember=form.remember_me.data)

        #用户登录成功后跳转到原先所要登录的页面
        next_page = request.args.get('next')
        #击者可以在next参数中插入一个指向恶意站点的URL，因此应用仅在重定向URL是相对路径时才执行重定向，这可确保重定向与应用保持在同一站点中。
        # 为了确定URL是相对的还是绝对的，我使用Werkzeug的url_parse()函数解析，然后检查netloc属性是否被设置
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)


#用户退出登录
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#用户注册功能
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html',title = 'Register', form=form)


#添加用户个人页
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user,'body':'Test post #1'},
        {'author':user,'body':'Test post #2'}
    ]
    return render_template('user.html',user=user,posts=posts)


#记录用户每次登录的时间，相当于给每次请求加了个中间件
@app.before_request
def before_requset():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


#编辑个人主页信息
@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():

    #form表单中传入参数，用来验证当前编辑的用户名
    form = EditProfileForm(current_user.username)
    '''
    当我们点击了表单上的提交按钮时，form.validate_on_submit()判断会做下面两件事情：
    1、通过is_submitted()通过判断HTTP方法来确认是否提交了表单
    2、通过WTForms提供的validate()来验证表单数据（使用我们在下面的表单类里给每个字段传入的验证函数）
    '''
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.about_me=form.about_me.data
        db.session.commit()
        flash('Your changes has been saved')
        return redirect(url_for('edit_profile'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.about_me.data=current_user.about_me
        return render_template('edit_profile.html',title='Edit Profile',form=form)


