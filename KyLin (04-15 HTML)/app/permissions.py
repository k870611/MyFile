from flask_principal import Permission, RoleNeed
from flask import render_template, jsonify
from functools import wraps
from app.models import Role

# Define Role
Manager = int(1) # Manager's auth in database is been set to int(1) and can't be changed
Operator = int(2)
Viewer = int(3)

manager_permission = Permission(RoleNeed(Manager))
operator_permission = Permission(RoleNeed(Operator))
viewer_permission = Permission(RoleNeed(Viewer))


def manager_authority(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if manager_permission.can():
            return func(*args, **kwargs)
        else:
            return render_template("cantInto.html")
    return decorated_view


def operator_authority(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if operator_permission.can():
            return func(*args, **kwargs)
        else:
            return render_template("cantInto.html")
    return decorated_view


def viewer_authorityForAjax(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not viewer_permission.can():
            return func(*args, **kwargs)
        else:
            return jsonify({'Viewer': 'True'})
    return decorated_view


def viewer_authority(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not viewer_permission.can():
            return func(*args, **kwargs)
        else:
            return render_template("cantInto.html")
    return decorated_view


def CanViewEvent_authority(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if manager_permission.can():
            role = Role.query.filter_by(role_auth=1).first()
            if role.role_event:
                return func(*args, **kwargs)
            else:
                return render_template("cantInto.html")

        elif operator_permission.can():
            role = Role.query.filter_by(role_auth=2).first()
            if role.role_event:
                return func(*args, **kwargs)
            else:
                return render_template("cantInto.html")

        elif viewer_permission.can():
            role = Role.query.filter_by(role_auth=3).first()
            if role.role_event:
                return func(*args, **kwargs)
            else:
                return render_template("cantInto.html")
        else:
            return render_template("cantInto.html")

    return decorated_view
