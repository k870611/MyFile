# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import UserMixin

from app import db
from app import login
from sqlalchemy.dialects.mysql import JSON


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(45))
    role_description = db.Column(db.String(250))
    role_group = db.Column(db.String(45))
    role_auth = db.Column(db.Integer)
    role_server = db.Column(db.Boolean)
    role_event = db.Column(db.Boolean)
    user = db.relationship('User', backref='role', lazy='dynamic')

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.id)  # python 3

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
    id = db.Column(db.Integer, primary_key=True)
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
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
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
            self.role_id = (Role.query.filter_by(role_auth=3).first()).id
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
        # self.acc_management_password = str(base64.b64encode(password.encode('utf-8')), 'utf-8')
        self.acc_management_password = password

    def check_password(self, password):

        # return check_password_hash(self.acc_management_password, password)
        # self.decodePwd = str(base64.b64decode(self.acc_management_password.encode('utf-8')), 'utf-8')

        if self.acc_management_password == password:
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
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    '''
    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.id)  # python 3

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
               'decodePwd {}>'.format(self.acc_management_account,
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
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(45))
    event_level = db.Column(db.String(45))
    event_name = db.Column(db.String(200))
    event_description = db.Column(db.String(250))
    event_time = db.Column(db.String(45))
    event_action = db.Column(db.String(250))
    sensor_type = db.Column(db.String(30))
    server_id = db.Column(db.Integer)
    sel_id = db.Column(db.Integer)

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.id)  # python 3

    def __repr__(self):
        return '<account {}, ' \
               'level {},' \
               'name {},' \
               'description {},' \
               'time {},' \
               'action {}>'.format(self.id,
                                   self.event_level,
                                   self.event_name,
                                   self.event_description,
                                   self.event_time,
                                   self.event_action)


class Server(db.Model):
    __tablename__ = 'server_info'
    id = db.Column(db.Integer, primary_key=True)
    server_slot = db.Column(db.String(45))
    server_ip = db.Column(db.String(45))
    server_mac = db.Column(db.String(45))
    server_update_time = db.Column(db.String(45))
    server_account = db.Column(db.String(100))
    server_password = db.Column(db.String(128))
    server_active = db.Column(db.Boolean)
    # insert_time = db.Column(db.DateTime, default=datetime.utcnow)
    # result = db.Column(JSON)
    tank_id = db.Column(db.Integer, db.ForeignKey('tank.id'))
    decodePwd = ''

    sdr = db.relationship('ServerSdr', backref='sdr', lazy='dynamic', cascade='delete')
    lan = db.relationship('ServerLan', backref='lan', lazy='dynamic', cascade='delete')
    fru = db.relationship('ServerFru', backref='fru', lazy='dynamic', cascade='delete')

    def get_id(self):
        # python 2 unicode(self.server_id)
            return str(self.server_id)  # python 3

    def set_password(self, password):
        # self.acc_management_password = generate_password_hash(password)
        # py 2 self.server_password = str(base64.b64encode(password.encode('utf-8')))
        # self.server_password = str(base64.b64encode(password.encode('utf-8')), 'utf-8')
        self.server_password = password

    def __repr__(self):
        return '<slot {}, ' \
               'ip {},' \
               'mac {},' \
               'status ,' \
               'tag ,' \
               'power ,' \
               'power_detail ,' \
               'degree ,' \
               'degree_detail ,' \
               'note , ' \
               'account {}, ' \
               'password {},' \
               'decodePwd {},' \
               'JSON ,' \
               'update_time{}>'.format(str(self.server_slot),
                                       self.server_ip,
                                       self.server_mac,
                                       self.server_account,
                                       self.server_password,
                                       self.decodePwd,
                                       self.server_update_time)


class ServerDetail(db.Model):
    __tablename__ = 'server_detail'
    id = db.Column(db.Integer, primary_key=True)
    server_tag = db.Column(db.String(250))
    server_note = db.Column(db.String(250))
    server_id = db.Column(db.Integer)


class ServerSdr(db.Model):

    __tablename__ = 'server_sdr_list_json'
    id = db.Column(db.Integer, primary_key=True)
    insert_time = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(JSON)
    server_id = db.Column(db.Integer, db.ForeignKey('server_info.id'))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.server_sdr_id)  # python 3

    def __repr__(self):
        return '<insert_time {}, result {}, server {} '.format(self.insert_time, self.result, self.server_id)


class ServerLan(db.Model):

    __tablename__ = 'server_lan_print_json'
    id = db.Column(db.Integer, primary_key=True)
    insert_time = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(JSON)
    server_id = db.Column(db.Integer, db.ForeignKey('server_info.id'))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.server_lan_id)  # python 3

    def __repr__(self):
        return '<insert_time {}, result {}, server {} '.format(self.insert_time, self.result, self.server_id)


class ServerFru(db.Model):

    __tablename__ = 'server_fru_json'
    id = db.Column(db.Integer, primary_key=True)
    insert_time = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(JSON)
    server_id = db.Column(db.Integer, db.ForeignKey('server_info.id'))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.server_fru_id)  # python 3

    def __repr__(self):
        return '<insert_time {}, result {}, server {} '.format(self.insert_time, self.result, self.server_id)


class ServerSelSaveJson(db.Model):

    __tablename__ = 'server_sel_save_json'
    id = db.Column(db.Integer, primary_key=True)
    insert_time = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(JSON)
    server_id = db.Column(db.Integer, db.ForeignKey('server_info.id'))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.server_fru_id)  # python 3

    def __repr__(self):
        return '<insert_time {}, result {}, server {} '.format(self.insert_time, self.result, self.server_id)



class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    log_module = db.Column(db.String(45))
    log_level = db.Column(db.String(45))
    log_description = db.Column(db.String(250))
    insert_time = db.Column(db.DateTime, default=datetime.utcnow)
    log_source = db.Column(db.String(45))
    log_user_account = db.Column(db.String(100))
    log_user_org = db.Column(db.String(100))

    def get_id(self):
        # python 2 unicode(self.server_id)
        return str(self.id)  # python 3

    def __init__(self, log_module, log_level, log_description, log_source, log_user_account, log_user_org, insert_time):
        self.log_module = log_module
        self.log_level = log_level
        self.log_description = log_description
        self.log_source = log_source
        self.insert_time = insert_time
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
                                    self.insert_time,
                                    self.log_source,
                                    self.log_user_account)


class Tank(db.Model):
    __tablename__ = 'tank'
    id = db.Column(db.Integer, primary_key=True)
    tank_name = db.Column(db.String(100))
    tank_description = db.Column(db.String(255))

    server = db.relationship('Server', backref='tank', lazy='dynamic', cascade='delete')

    def __repr__(self):
        return '<tank_name {}, tank_description {}'.format(self.tank_name, self.tank_description)


class Alarm(db.Model):
    __tablename__ = 'alarm'
    id = db.Column(db.Integer, primary_key=True)
    alarm_enable = db.Column(db.Boolean)
    alarm_name = db.Column(db.String(45))
    alarm_description = db.Column(db.String(255))
    alarm_level = db.Column(db.String(45))
    alarm_condition = db.Column(db.String(45))
    alarm_value = db.Column(db.Float)
    sensor_name = db.Column(db.String(45))

    def __repr__(self):
        return '<alarm_name {}, ' \
               'alarm_description {}, ' \
               'alarm_level {},' \
               'alarm_condition {},' \
               'alarm_value {},' \
               'sensor_name {}.'.format(self.alarm_name,
                                        self.alarm_description,
                                        self.alarm_level,
                                        self.alarm_condition,
                                        self.alarm_value,
                                        self.sensor_name)


class ServerSelSaveList(db.Model):
    __tablename__ = 'server_sel_save_list'

    id = db.Column(db.Integer, primary_key=True)
    insert_time = db.Column(db.DateTime, default=datetime.utcnow)
    sensor_type = db.Column(db.String(30))
    event_detail = db.Column(db.String(30))
    server_id = db.Column(db.Integer)
    sel_id = db.Column(db.String(11))
    sel_day = db.Column(db.String(32))
    sel_time = db.Column(db.String(32))
    sel_name = db.Column(db.String(128))
    sel_description = db.Column(db.String(256))
    sel_tag = db.Column(db.String(100))

    def __repr__(self):
        return '<insert_time {}, ' \
               'sensor_type {}, ' \
               'event_detail {},' \
               'server_id {},' \
               'sel_id {},' \
               'sel_day {}, ' \
               'sel_time {}, ' \
               'sel_name {}, ' \
               'sel_description {}, ' \
               'sel_tag {},'.format(self.insert_time,
                                    self.sensor_type,
                                    self.event_detail,
                                    self.server_id,
                                    self.sel_id,
                                    self.sel_day,
                                    self.sel_time,
                                    self.sel_name,
                                    self.sel_description,
                                    self.sel_tag)


class ServerChassisStatusJson(db.Model):

    __tablename__ = 'server_chassis_status_json'
    ID = db.Column(db.Integer, primary_key=True)
    insert_time = db.Column(db.DateTime, default=datetime.utcnow)
    server_id = db.Column(db.Integer)
    result = db.Column(JSON)

    def __repr__(self):
        return '<insert_time {}, result {}, server {} '.format(self.insert_time, self.result, self.server_id)

