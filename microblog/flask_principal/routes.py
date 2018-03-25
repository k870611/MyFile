from app import app
from flask import request
from flask_login import login_user
from flask_principal import current_app, identity_changed, Identity
from app import app, db
from userinfo import User


@app.route("/login",methods=["POST"])
def login():
    user = request.form.get("user",None)
    password = request.form.get("password",None)
    if not user or not password:
        print 'aa'
    user = db.session.query(User).filter_by(user=user,password=password).first()
    if not user:
        print 'bb'
    # 登录
    login_user(user)
    # 发送信号，载入用户权限
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

    from app import app
    from permission import admin_authority

    @app.route("/delete_user", methods=["POST"])
    @admin_authority
    def delete_user():
        print 'delete'
