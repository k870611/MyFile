from flask_principal import Permission, RoleNeed
from functools import wraps
# 定义相关角色
NORMAL = "NORMAL"
ADMIN = "ADMIN"
ROLES = (
    ("NORMAL", "普通用户"),
    ("ADMIN", "管理员")
)

admin_permission = Permission(RoleNeed(ADMIN))


def admin_authority(func):
    @wraps
    def decorated_view(*args, **kwargs):
        if admin_permission.can():
            return func(*args, **kwargs)
        else:
            return "非Admin用户"
    return decorated_view
