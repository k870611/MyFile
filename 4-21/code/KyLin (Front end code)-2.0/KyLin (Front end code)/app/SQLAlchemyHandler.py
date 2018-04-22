from flask import request
from flask_login import current_user
from app.models import Log
from app import db
import logging
import socket


class SQLAlchemyHandler(logging.Handler):
    def emit(self, record):

        my_computer_name = socket.getfqdn(socket.gethostname())
        ip = socket.gethostbyname(my_computer_name)

        Server = 'Server'
        Event = 'Event'
        Account = 'Account'
        Role = 'Role'
        IPMI = 'IPMI'
        Tank = 'Tank'

        path = {'serverinfo': Server,
                'ChangeFunctionTag': Server,
                'ChangeServerNote': Server,
                'eventlist': Event,
                'accountCreate': Account,
                'accountModify': Account,
                'accountDelete': Account,
                'roleModify': Role,
                'AddAccIntoRole': Role,
                'DelRoleAcc': Role,
                'ChangeViewByAjax': Role,
                'IpmiModify': Tank,
                'IpmiDelete': Tank,
                'AddTank': Tank,
                'ModifyTank': Tank,
                'DeleteTank': Tank,
                'AddServer': Tank,
                'DelServerFromTank': Tank}.get(str(request.path).replace('/', ''), '')

        logger = Log(log_module=path,
                     log_level=record.__dict__['levelname'],
                     log_description=record.__dict__['msg'],
                     log_source=ip,
                     log_user_account=current_user.acc_management_account,
                     log_user_org=current_user.acc_management_organization)

        db.session.add(logger)
        db.session.commit()
