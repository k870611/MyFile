from app import db, models
from sqlalchemy import desc

u = models.User(nickname='john', email='john@email.com')
db.session.add(u)
db.session.commit()

u = models.User(nickname='susan', email='susan@email.com')
db.session.add(u)
db.session.commit()

users = models.User.query.all()
users
for u in users:
    print(u.id, u.nickname)

u = models.User.query.get(1)
u

import datetime
u = models.User.query.get(1)
p = models.Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=u)
db.session.add(p)
db.session.commit()

u = models.User.query.get(1)
u
posts = u.posts.all()
posts
for p in posts:
    print(p.id, p.author.nickname, p.body)

u = models.User.query.get(2)
u
u.posts.all()
models.User.query.order_by('nickname desc').all()

users = models.User.query.all()
for u in users:
    db.session.delete(u)

posts = models.Post.query.all()
for p in posts:
    db.session.delete(p)

db.session.commit()



