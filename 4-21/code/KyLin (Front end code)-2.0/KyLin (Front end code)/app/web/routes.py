# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_principal import current_app, identity_changed, Identity, AnonymousIdentity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from app.models import User, EventWarning, EventDevice, EventSystem, EventNow, Server, Role, Log, Tank
from app import app, db
from app.forms import LoginForm, AccountCreateForm, AccountModifyForm, RoleModifyForm, AddTankForm, ModifyTankForm
from app.permissions import manager_authority, CanViewEvent_authority
from app import Manager_is_login

import base64
import sys
from datetime import datetime
import datetime as date
import re
import sqlalchemy


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    global Manager_is_login

    if current_user.is_authenticated:
        return redirect(url_for('serverinfo'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(acc_management_account=form.userName.data).first()

        if user.role_id == 1 and Manager_is_login:
            lastManager = User.query.filter_by(role_id=1).order_by(User.acc_management_operate_date.desc()).first()
            deadline = lastManager.acc_management_operate_date + date.timedelta(minutes=+10)

            if datetime.now() < deadline:
                flash('Sorry, Only one Manager can into is System.')
                return redirect(url_for('login'))

        if user is None or not user.check_password(form.password.data):
            flash('Sorry, Your UserName or Password is wrong, please try again.')
            return redirect(url_for('login'))

        if user.acc_management_active is False:
            flash('Sorry, Your account is inactive')
            return redirect(url_for('login'))

        if len(user.acc_management_acc_deadline) >= 10:
            accDeadline = re.sub('\s', '', str(user.acc_management_acc_deadline)).split('~')

            dateFrom = datetime.strptime(accDeadline[0] + ' 00:00', '%Y-%m-%d %H:%M')
            dateTo = datetime.strptime(accDeadline[1] + ' 23:59', '%Y-%m-%d %H:%M')

            if (datetime.now() < dateFrom) or (datetime.now() > dateTo):
                flash('Sorry, Your account is expired')
                return redirect(url_for('login'))

        login_user(user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.acc_management_id))
        Manager_is_login = True
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('serverinfo')

        return redirect(next_page)

    return render_template("Login.html", form=form)


@app.route('/serverinfo')
@login_required
def serverinfo():
    tank = Tank.query.order_by(Tank.tank_name).all()
    tank_id = tank[0].tank_id

    server = Server.query.filter(Server.tank_id == tank_id, Server.server_active == True).order_by(Server.server_slot).all()

    '''
    record = Server.query.filter(Server.server_json["id"] >= 0).all()

    for r in record:
        print(r)

    info = []

    for s in server:
        if s.server_json is not None:
            if type(s.server_json) is dict:
                info.append(s.server_json)

            elif type(s.server_json) is list:
                info.append(s.server_json[0])

    print(info)
    '''

    EventCount = CountEventNow()

    return render_template("serverinfo.html",
                           filter='slot',
                           value='',
                           tank_list=tank,
                           server_list=server,
                           CountEventNow=EventCount,
                           tank_value=tank_id)


@app.route('/eventlist')
@login_required
@CanViewEvent_authority
def eventlist():

    eventWarning = EventWarning.query.all()
    eventDevice = EventDevice.query.all()
    eventSystem = EventSystem.query.all()
    eventNow = EventNow.query.all()
    EventList = []

    for e in eventWarning:
        EventList.append({
            'table': 'event_warning',
            'level': e.event_warning_level,
            'name': e.event_warning_name,
            'description': e.event_warning_description,
            'time': e.event_warning_time,
            'action': e.event_warning_action,
        })

    for e in eventDevice:
        EventList.append({
            'table': 'event_device',
            'level': e.event_device_level,
            'name': e.event_device_name,
            'description': e.event_device_description,
            'time': e.event_device_time,
            'action': e.event_device_action,
        })

    for e in eventSystem:
        EventList.append({
            'table': 'event_system',
            'level': e.event_system_level,
            'name': e.event_system_name,
            'description': e.event_system_description,
            'time': e.event_system_time,
            'action': e.event_system_action,
        })

    for e in eventNow:
        EventList.append({
            'table': 'event_now',
            'level': e.event_now_level,
            'name': e.event_now_name,
            'description': e.event_now_description,
            'time': e.event_now_time,
            'action': e.event_now_action,
        })

    EventCount = CountEventNow()

    return render_template("eventlist.html", EventList=EventList, ShowInfo='all', CountEventNow=EventCount)


@app.route('/accmanagement', methods=['GET', 'POST'])
@login_required
@manager_authority
def accmanagement():

    page = request.args.get('page', 1, type=int)
    click = request.args.get('click', '')

    rowTotal = len(User.query.all())

    if rowTotal % app.config["DATA_PER_PAGE"] is 0:
        pageTotal = int(rowTotal // app.config["DATA_PER_PAGE"])
    else:
        pageTotal = int(rowTotal // app.config["DATA_PER_PAGE"])+1

    if click == 'b':
        page = 1
    elif click == 'e':
        page = pageTotal

    users = User.query.order_by(User.acc_management_account).paginate(page, app.config["DATA_PER_PAGE"], False)
    i = 0
    for u in users.items:
        if float(sys.version[:3]) < 3:
            users.items[i].decodePwd = base64.b64decode(u.acc_management_password.encode('utf-8'))

        else:
            users.items[i].decodePwd = str(base64.b64decode(u.acc_management_password.encode('utf-8')), 'utf-8')

        i += 1

    prev_url = url_for('accmanagement', page=users.prev_num) if users.has_prev else None
    next_url = url_for('accmanagement', page=users.next_num) if users.has_next else None

    accountCreate = AccountCreateForm()
    accountModify = AccountModifyForm()

    myFilter = 'account'

    EventCount = CountEventNow()

    return render_template("accmanagement.html",
                           acc_info=users.items,
                           accountCreate=accountCreate,
                           accountModify=accountModify,
                           accountAction='init',
                           prev_url=prev_url,
                           next_url=next_url,
                           rowTotal=rowTotal,
                           pageTotal=pageTotal,
                           page=page,
                           filter=myFilter,
                           value='',
                           CountEventNow=EventCount)


@app.route('/role')
@login_required
@manager_authority
def role():
    roleModifyForm = RoleModifyForm()
    roleList = Role.query.order_by(Role.role_name).all()
    EventCount = CountEventNow()

    return render_template("role.html",
                           CountEventNow=EventCount,
                           roleList=roleList,
                           roleModifyForm=roleModifyForm,
                           Action='init',
                           value='')


@app.route('/online')
@login_required
@manager_authority
def online():
    page = request.args.get('page', 1, type=int)
    deadline = datetime.now() + date.timedelta(minutes=-30)

    users = User.query.filter(User.acc_management_operate_date > deadline).order_by(User.acc_management_operate_date.desc())
    rowTotal = len([u for u in users])

    if rowTotal % app.config["DATA_PER_PAGE"] is 0:
        pageTotal = int(rowTotal // app.config["DATA_PER_PAGE"])
    else:
        pageTotal = int(rowTotal // app.config["DATA_PER_PAGE"]) + 1

    users = users.paginate(page, app.config["DATA_PER_PAGE"], False)

    prev_url = url_for('online', page=users.prev_num) if users.has_prev else None
    next_url = url_for('online', page=users.next_num) if users.has_next else None

    myFilter = 'account'

    EventCount = CountEventNow()
    return render_template("OnlineUser.html",
                           acc_info=users.items,
                           prev_url=prev_url,
                           next_url=next_url,
                           rowTotal=rowTotal,
                           pageTotal=pageTotal,
                           page=page,
                           filter=myFilter,
                           value='',
                           CountEventNow=EventCount)


@app.route('/itmanagement')
@login_required
@manager_authority
def itmanagement():

    page = request.args.get('page', 1, type=int)
    click = request.args.get('click', '')

    rowTotal = len(Server.query.all())

    if rowTotal % app.config["DATA_PER_PAGE"] is 0:
        pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"])
    else:
        pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"]) + 1

    if click == 'b':
        page = 1
    elif click == 'e':
        page = pageTotal

    server = Server.query.order_by(Server.server_slot).paginate(page, app.config["DATA_PER_PAGE"], False)
    i = 0
    for s in server.items:
        s.decodePwd = str(base64.b64decode(s.server_password.encode('utf-8')), 'utf-8')
        i += 1

    prev_url = url_for('itmanagement', page=server.prev_num) if server.has_prev else None
    next_url = url_for('itmanagement', page=server.next_num) if server.has_next else None

    EventCount = CountEventNow()
    return render_template("itmanagement.html", CountEventNow=EventCount, server_list=server.items,
                           prev_url=prev_url,
                           next_url=next_url,
                           rowTotal=rowTotal,
                           pageTotal=pageTotal,
                           page=page,
                           select='ip',
                           value='')


@app.route('/tankManagement')
@login_required
@manager_authority
def tankManagement():

    addTankForm = AddTankForm()
    modifyTankForm = ModifyTankForm()
    tankList = Tank.query.order_by(Tank.tank_name).all()
    EventCount = CountEventNow()

    return render_template("tank.html",
                           CountEventNow=EventCount,
                           tankList=tankList,
                           addTankForm=addTankForm,
                           modifyTankForm=modifyTankForm,
                           Action='init',
                           value='')


@app.route('/log')
@login_required
@manager_authority
def log():
    page = request.args.get('page', 1, type=int)
    click = request.args.get('click', '')

    arySearch = []

    rowTotal = len(Log.query.all())

    if rowTotal % app.config["DATA_PER_PAGE"] is 0:
        pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"])
    else:
        pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"]) + 1

    if click == 'b':
        page = 1
    elif click == 'e':
        page = pageTotal

    logs = Log.query.order_by(Log.log_date.desc()).paginate(page, app.config["DATA_PER_PAGE"], False)

    prev_url = url_for('log', page=logs.prev_num) if logs.has_prev else None
    next_url = url_for('log', page=logs.next_num) if logs.has_next else None

    EventCount = CountEventNow()
    return render_template("log.html", CountEventNow=EventCount, log_list=logs.items,
                           prev_url=prev_url,
                           next_url=next_url,
                           rowTotal=rowTotal,
                           pageTotal=pageTotal,
                           page=page,
                           arySearch=arySearch)


@app.route('/logout')
def logout():
    global Manager_is_login
    Manager_is_login = False

    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('login'))


@app.route('/cantInto')
def cantInto():
    return render_template("cantInto.html")


def CountEventNow():
    Count = len(EventNow.query.all())
    return Count


@app.after_request
def after_request(response):
    session.permanent = True
    app.permanent_session_lifetime = date.timedelta(minutes=10)

    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        if current_user.is_authenticated:
            current_user.acc_management_operate_date = datetime.now()
            try:
                db.session.commit()

            except SQLAlchemy.exc.SQLAlchemyError:
                db.session.rollback()

    return response



