# -*- coding: utf-8 -*-
import base64
from datetime import datetime
from flask_login import UserMixin

from app import db
from app import login
# from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(45))
    role_description = db.Column(db.String(250))
    role_group = db.Column(db.String(45))
    role_auth = db.Column(db.Integer)
    role_server = db.Column(db.Boolean)
    role_event = db.Column(db.Boolean)
    user = db.relationship('User', backref='role', lazy='dynamic')

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.role_id)  # python 3

    def __repr__(self):
        return '<name {},' \
               'description {},' \
               'group {},' \
               'server {}, ' \
               'event {}' \
               'auth {}>'.format(self.role_name,
                                 self.role_description,
                                 self.role_group,
                                 self.role_server,
                                 self.role_event,
                                 self.role_auth)


class User(UserMixin, db.Model):
    __tablename__ = 'acc_management'
    acc_management_id = db.Column(db.Integer, primary_key=True)
    acc_management_account = db.Column(db.String(100))
    acc_management_name = db.Column(db.String(100))
    acc_management_password = db.Column(db.String(128))
    acc_management_organization = db.Column(db.String(100))
    acc_management_email = db.Column(db.String(100))
    acc_management_phone = db.Column(db.String(45))
    acc_management_active = db.Column(db.Boolean)
    acc_management_acc_deadline = db.Column(db.String(45))
    acc_management_org_manager = db.Column(db.Boolean)
    acc_management_operate_date = db.Column(db.DateTime, default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    decodePwd = ''

    def __init__(self,
                 acc_management_account,
                 acc_management_name,
                 acc_management_password,
                 acc_management_organization,
                 acc_management_email,
                 acc_management_phone,
                 acc_management_active,
                 acc_management_acc_deadline,
                 acc_management_org_manager):

        if self.role_id is None:
            self.role_id = (Role.query.filter_by(role_auth=3).first()).role_id
            self.acc_management_account = acc_management_account
            self.acc_management_name = acc_management_name
            self.acc_management_password = acc_management_password
            self.acc_management_organization = acc_management_organization
            self.acc_management_email = acc_management_email
            self.acc_management_phone = acc_management_phone
            self.acc_management_active = acc_management_active
            self.acc_management_acc_deadline = acc_management_acc_deadline
            self.acc_management_org_manager = acc_management_org_manager

    def set_password(self, password):
        # self.acc_management_password = generate_password_hash(password)
        # self.acc_management_password = str(base64.b64encode(password.encode('utf-8'))) py -2
        self.acc_management_password = str(base64.b64encode(password.encode('utf-8')), 'utf-8')

    def check_password(self, password):

        # return check_password_hash(self.acc_management_password, password)
        self.decodePwd = str(base64.b64decode(self.acc_management_password.encode('utf-8')), 'utf-8')

        if self.decodePwd == password:
            return True
        else:
            return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    '''
    def get_id(self):
        try:
            return unicode(self.acc_management_id)  # python 2
        except NameError:
            return str(self.acc_management_id)  # python 3
    '''
    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.acc_management_id)  # python 3

    def __repr__(self):
        return '<account {}, ' \
               'name {},' \
               'password {},' \
               'organization {},' \
               'email {},' \
               'phone {},' \
               'active {},' \
               'deadline {},' \
               'org_manager {},' \
               'role_id {}, ' \
               'decodePWd {}>'.format(self.acc_management_account,
                                      self.acc_management_name,
                                      self.acc_management_password,
                                      self.acc_management_organization,
                                      self.acc_management_email,
                                      self.acc_management_phone,
                                      self.acc_management_active,
                                      self.acc_management_acc_deadline,
                                      self.acc_management_org_manager,
                                      self.role_id,
                                      self.decodePwd)


class EventWarning(db.Model):
    __tablename__ = 'event_warning'
    event_warning_id = db.Column(db.Integer, primary_key=True)
    event_warning_level = db.Column(db.String(45))
    event_warning_name = db.Column(db.String(200))
    event_warning_description = db.Column(db.String(250))
    event_warning_time = db.Column(db.String(45))
    event_warning_action = db.Column(db.String(250))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.event_warning_id)  # python 3

    def __repr__(self):
        return '<account {}, ' \
               'level {},' \
               'name {},' \
               'description {},' \
               'time {},' \
               'action {}>'.format(self.event_warning_id,
                                   self.event_warning_level,
                                   self.event_warning_name,
                                   self.event_warning_description,
                                   self.event_warning_time,
                                   self.event_warning_action)


class EventDevice(db.Model):
    __tablename__ = 'event_device'
    event_device_id = db.Column(db.Integer, primary_key=True)
    event_device_level = db.Column(db.String(45))
    event_device_name = db.Column(db.String(200))
    event_device_description = db.Column(db.String(250))
    event_device_time = db.Column(db.String(45))
    event_device_action = db.Column(db.String(250))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.event_device_id)  # python 3

    def __repr__(self):
        return '<account {}, ' \
               'level {},' \
               'name {},' \
               'description {},' \
               'time {},' \
               'action {}>'.format(self.event_device_id,
                                   self.event_device_level,
                                   self.event_device_name,
                                   self.event_device_description,
                                   self.event_device_time,
                                   self.event_device_action)


class EventSystem(db.Model):
    __tablename__ = 'event_system'
    event_system_id = db.Column(db.Integer, primary_key=True)
    event_system_level = db.Column(db.String(45))
    event_system_name = db.Column(db.String(200))
    event_system_description = db.Column(db.String(250))
    event_system_time = db.Column(db.String(45))
    event_system_action = db.Column(db.String(250))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.event_system_id)  # python 3

    def __repr__(self):
        return '<account {}, ' \
               'level {},' \
               'name {},' \
               'description {},' \
               'time {},' \
               'action {}>'.format(self.event_system_id,
                                   self.event_system_level,
                                   self.event_system_name,
                                   self.event_system_description,
                                   self.event_system_time,
                                   self.event_system_action)


class EventNow(db.Model):
    __tablename__ = 'event_now'
    event_now_id = db.Column(db.Integer, primary_key=True)
    event_now_level = db.Column(db.String(45))
    event_now_name = db.Column(db.String(200))
    event_now_description = db.Column(db.String(250))
    event_now_time = db.Column(db.String(45))
    event_now_action = db.Column(db.String(250))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.event_now_id)  # python 3

    def __repr__(self):
        return '<account {}, ' \
               'level {},' \
               'name {},' \
               'description {},' \
               'time {},' \
               'action {}>'.format(self.event_now_id,
                                   self.event_now_level,
                                   self.event_now_name,
                                   self.event_now_description,
                                   self.event_now_time,
                                   self.event_now_action)


class Server(db.Model):
    __tablename__ = 'server'
    server_id = db.Column(db.Integer, primary_key=True)
    server_slot = db.Column(db.String(45))
    server_ip = db.Column(db.String(45))
    server_mac = db.Column(db.String(45))
    server_status = db.Column(db.Integer)
    server_tag = db.Column(db.String(250))
    server_power = db.Column(db.String(45))
    server_power_detail = db.Column(db.String(250))
    server_degree = db.Column(db.String(45))
    server_degree_detail = db.Column(db.String(250))
    server_note = db.Column(db.String(250))
    server_update_time = db.Column(db.String(45))
    server_account = db.Column(db.String(100))
    server_password = db.Column(db.String(128))
    decodePwd = ''

    sdr = db.relationship('ServerSdr', backref='sdr', lazy='dynamic')
    lan = db.relationship('ServerLan', backref='lan', lazy='dynamic')
    fru = db.relationship('ServerFru', backref='fru', lazy='dynamic')

    def get_id(self):
        # python 2 unicode(self.server_id)
            return str(self.server_id)  # python 3

    def set_password(self, password):
        # self.acc_management_password = generate_password_hash(password)
        # py 2 self.server_password = str(base64.b64encode(password.encode('utf-8')))
        self.server_password = str(base64.b64encode(password.encode('utf-8')), 'utf-8')

    def __repr__(self):
        return '<slot {}, ' \
               'ip {},' \
               'mac {},' \
               'status {},' \
               'tag {},' \
               'power {},' \
               'power_detail {},' \
               'degree {},' \
               'degree_detail {},' \
               'note {}, ' \
               'account {}, ' \
               'password {},' \
               'decodePwd {}, ' \
               'update_time{}>'.format(str(self.server_slot),
                                       self.server_ip,
                                       self.server_mac,
                                       self.server_status,
                                       self.server_tag,
                                       self.server_power,
                                       self.server_power_detail,
                                       self.server_degree,
                                       self.server_degree_detail,
                                       self.server_note,
                                       self.server_account,
                                       self.server_password,
                                       self.decodePwd,
                                       self.server_update_time)


class ServerSdr(db.Model):
    __tablename__ = 'server_sdr'
    server_sdr_id = db.Column(db.Integer, primary_key=True)
    server_sdr_name = db.Column(db.String(45))
    server_sdr_status = db.Column(db.String(45))
    server_sdr_value = db.Column(db.String(45))
    server_id = db.Column(db.Integer, db.ForeignKey('server.server_id'))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.server_sdr_id)  # python 3

    def __repr__(self):
        return '<name {}, ' \
               'status {},' \
               'value {},>'.format(self.server_sdr_name,
                                   self.server_sdr_status,
                                   self.server_sdr_value)


class ServerLan(db.Model):
    __tablename__ = 'server_lan'
    server_lan_id = db.Column(db.Integer, primary_key=True)
    server_lan_name = db.Column(db.String(45))
    server_lan_value = db.Column(db.String(45))
    server_id = db.Column(db.Integer, db.ForeignKey('server.server_id'))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.server_lan_id)  # python 3

    def __repr__(self):
        return '<name {}, ' \
               'value {},>'.format(self.server_sdr_name,
                                   self.server_sdr_value)


class ServerFru(db.Model):
    __tablename__ = 'server_fru'
    server_fru_id = db.Column(db.Integer, primary_key=True)
    server_fru_name = db.Column(db.String(45))
    server_fru_value = db.Column(db.String(45))
    server_id = db.Column(db.Integer, db.ForeignKey('server.server_id'))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.server_fru_id)  # python 3

    def __repr__(self):
        return '<name {}, ' \
               'value {},>'.format(self.server_fru_name,
                                   self.server_fru_value)


class Log(db.Model):
    __tablename__ = 'log'
    log_id = db.Column(db.Integer, primary_key=True)
    log_module = db.Column(db.String(45))
    log_level = db.Column(db.String(45))
    log_description = db.Column(db.String(250))
    log_date = db.Column(db.DateTime, default=datetime.utcnow)
    log_source = db.Column(db.String(45))
    log_user_account = db.Column(db.String(100))
    log_user_org = db.Column(db.String(100))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.log_id)  # python 3

    def __init__(self, log_module, log_level, log_description, log_source, log_user_account, log_user_org):
        self.log_module = log_module
        self.log_level = log_level
        self.log_description = log_description
        self.log_source = log_source
        self.log_date = datetime.now()
        self.log_user_account = log_user_account
        self.log_user_org = log_user_org

    def __repr__(self):
        return '<module {}, ' \
               'level {}, ' \
               'description {}, ' \
               'date {}, ' \
               'source {}, ' \
               'uAccount{}>'.format(self.log_module,
                                    self.log_level,
                                    self.log_description,
                                    self.log_date,
                                    self.log_source,
                                    self.log_user_account)










