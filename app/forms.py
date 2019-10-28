# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo,Length
from app.models import User

#登录表单
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField('Repeat ')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Sign In")

#用户注册页面表单
class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email(message=u"请输入有效的邮箱地址，比如：username@domain.com")])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


#编辑个人主页信息表单
class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0,max=140)])
    submit = SubmitField("提交")

    '''
    RegistrationForm已经实现了对用户名的验证，但是编辑表单的要求稍有不同。 
    在注册期间，我需要确保在表单中输入的用户名不存在于数据库中。 在编辑个人资料表单中，我必须做同样的检查，但有一个例外。 
    如果用户不改变原始用户名，那么验证应该允许，因为该用户名已经被分配给该用户。
    '''
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm,self).__init__(*args, **kwargs)
        self.original_uername = original_username

    def validate_uername(self, username):
        if username.data != self.original_uername:
            user = User.query.filter_by(username = self.username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username")