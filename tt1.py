# -*- coding:utf-8 -*-

from app import db
from app.models import User,Post

# u = User(username='jake', email='jake@example.com')
# u.set_password('jake123')
# db.session.add(u)
# db.session.commit()


# users = User.query.all()
# print(users)
# for u in users:
#     print(u.id,u.username)


# n = User.query.get(2)
# print(n)
# p = Post(body="my first post!", author=n)
# db.session.add(p)
# db.session.commit()

username="jake"
u = User.query.filter_by(username=username.data).first()
if u is None:
    print('aaaa')
