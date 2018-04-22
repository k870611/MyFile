from flask import render_template, flash, request, jsonify
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

from app import app, db
from app.permissions import manager_authority
from app.models import EventNow, Tank, Server
from app.forms import AddTankForm, ModifyTankForm
import base64
from datetime import datetime


@app.route('/AddTank', methods=['GET', 'POST'])
@login_required
@manager_authority
def AddTank():

    addTankForm = AddTankForm()
    modifyTankForm = ModifyTankForm()
    tankAddSuccess = False

    if addTankForm.validate_on_submit():

        tank = Tank(tank_name=addTankForm.name.data, tank_description=addTankForm.description.data)

        try:
            db.session.add(tank)
            db.session.commit()
            flash('Create Tank Success!')
            app.logger.info("Create " + addTankForm.name.data + " tank successfully.")

            tankAddSuccess = True

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to create " + addTankForm.name.data + " tank.")

    tankList = Tank.query.order_by(Tank.tank_name).all()
    EventCount = CountEventNow()

    if tankAddSuccess is not True:
        flash('Sorry, Create Tank failed. Please try again!')

    return render_template("tank.html",
                           CountEventNow=EventCount,
                           tankList=tankList,
                           addTankForm=addTankForm,
                           modifyTankForm=modifyTankForm,
                           Action='create',
                           value='')


@app.route('/ModifyTank', methods=['GET', 'POST'])
@login_required
@manager_authority
def ModifyTank():

    addTankForm = AddTankForm()
    modifyTankForm = ModifyTankForm()
    tankModifySuccess = False

    if modifyTankForm.validate_on_submit():

        tank = Tank.query.filter_by(tank_name=modifyTankForm.originalTank.data).first()
        tank.tank_name = modifyTankForm.name.data
        tank.tank_description = modifyTankForm.description.data

        try:
            db.session.commit()
            flash('Modify Tank Success!')
            app.logger.info("Modify " + modifyTankForm.name.data + " successfully.")

            tankModifySuccess = True

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to modify " + addTankForm.name.data + " tank.")

    tankList = Tank.query.order_by(Tank.tank_name).all()
    EventCount = CountEventNow()

    if tankModifySuccess is not True:
        flash('Sorry, Create Tank failed. Please try again!')

    return render_template("tank.html",
                           CountEventNow=EventCount,
                           tankList=tankList,
                           addTankForm=addTankForm,
                           modifyTankForm=modifyTankForm,
                           Action='modify',
                           value='')


@app.route('/DeleteTank', methods=['GET', 'POST'])
@login_required
@manager_authority
def DeleteTank():

    t = request.form.get('tank', '')

    tank = Tank.query.filter_by(tank_name=t).first()

    try:

        db.session.delete(tank)
        db.session.commit()

        app.logger.info("Delete " + tank.tank_name + " tank successfully.")

        deleteInfo = 'true'

    except SQLAlchemy.exc.SQLAlchemyError:
        app.logger.exception("Fail to delete " + tank.tank_name + " tank.")

    return jsonify({'tank': t, 'deleteInfo': deleteInfo})


@app.route('/GetServerByAjax', methods=['GET', 'POST'])
@login_required
@manager_authority
def GetServerByAjax():
    page = request.args.get('page', 1, type=int)
    tank = request.args.get('tank', '')

    select = request.args.get('select', '')
    text = request.args.get('text', '')

    if select == 'ip':
        server = Server.query.join(Tank).filter(Server.server_ip.like('%'+text+'%'), Tank.tank_name.like('%'+tank+'%'))\
            .order_by(Server.server_active, Server.server_slot)

    elif select == 'mac':
        server = Server.query.join(Tank).filter(Server.server_mac.like('%'+text+'%'), Tank.tank_name.like('%'+tank+'%'))\
            .order_by(Server.server_active, Server.server_slot)

    else:
        server = Server.query.join(Tank).filter(Tank.tank_name.like('%'+tank+'%')).order_by(Server.server_active, Server.server_slot)

    if server is None:
        return jsonify({'Success': 'False'})

    rowCount = len([u for u in server])

    if rowCount % app.config["DATA_PER_PAGE"] is 0:
        totalPage = int(rowCount // app.config["DATA_PER_PAGE"])
    else:
        totalPage = int(rowCount / app.config["DATA_PER_PAGE"]) + 1

    server = server.paginate(page, app.config["DATA_PER_PAGE"], False)

    serverInfo = {}
    i = 0
    for u in server.items:
        pwd = str(base64.b64decode(u.server_password.encode('utf-8')), 'utf-8')
        serverInfo[i] = {
            'slot': u.server_slot,
            'ip': u.server_ip,
            'mac': u.server_mac,
            'tag': u.server_tag,
            'acc': u.server_account,
            'pwd': pwd,
            'note': u.server_note,
            'active': u.server_active}
        i += 1

    return jsonify({'Success': 'True', 'userInfo': serverInfo, 'totalPage': totalPage, 'totalRow': rowCount, 'page': page})


@app.route('/AddServer', methods=['GET', 'POST'])
@login_required
@manager_authority
def AddServer():

    tank_name = request.get_json(force=True).get('tank_name')
    acc = request.get_json(force=True).get('acc')

    if tank_name is None or tank_name == '':
        return jsonify({'Success': 'False'})

    for i in acc:
        if i == '' or i is None:
            continue

        server = Server.query.filter_by(server_mac=i).first()
        tank = Tank.query.filter_by(tank_name=tank_name).first()

        if server is None:
            continue

        server.tank_id = tank.tank_id

        try:
            db.session.commit()
            app.logger.info("Add server " + server.server_mac + " into tank "+tank_name+".")

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to add server "+server.server_mac+" into tank "+tank_name+".")

    return jsonify({'Success': 'True'})


@app.route('/IpmiModify', methods=['GET', 'POST'])
@login_required
@manager_authority
def IpmiModify():
    slot = request.form.get('slot', '')
    ip = request.form.get('ip', '')
    account = request.form.get('account', '')
    password = request.form.get('password', '')
    mac = request.form.get('mac', '')
    tag = request.form.get('tag', '')
    memo = request.form.get('memo', '')
    orgMac = request.form.get('orgMac', '')
    active = request.form.get('active', '')
    print(active)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    server = Server.query.filter_by(server_mac=orgMac).first()

    if server is None:
        return jsonify({'Success': 'False'})

    server.server_slot = slot
    server.server_ip = ip
    server.server_account = account
    server.server_mac = mac
    server.server_tag = tag
    server.server_note = memo

    if active == 'false':
        server.server_active = False
    else:
        server.server_active = True

    server.server_update_time = now

    server.set_password(password)

    try:
        db.session.commit()
        app.logger.info("Modify server" + server.server_ip + " IPMI successfully.")

    except SQLAlchemy.exc.SQLAlchemyError:
        app.logger.exception("Fail to Modify " + server.server_ip + ".")

    return jsonify({'Success': 'True'})


@app.route('/DelServerFromTank', methods=['GET', 'POST'])
@login_required
@manager_authority
def DelServerFromTank():

    tank_name = request.get_json(force=True).get('tank_name')
    acc = request.get_json(force=True).get('acc')

    for i in acc:
        if i == '' or i is None:
            continue

        server = Server.query.filter_by(server_mac=i).first()

        if server is None:
            continue

        server.server_ip = ''
        server.server_mac = ''
        server.server_status = 0
        server.server_tag = ''
        server.server_note = ''
        server.server_power = ''
        server.server_power_detail = ''
        server.server_degree = ''
        server.server_degree_detail = ''
        server.server_note = ''
        server.server_update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        server.server_account = ''
        server.server_password = ''
        server.server_active = 0

        try:
            db.session.commit()
            app.logger.info("Delete server " + server.server_mac + " from tank " + tank_name + ".")

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to delete server "+server.server_mac+" from role "+tank_name+".")

    return jsonify({'Success': 'True'})


@app.route('/TankSearch', methods=['GET', 'POST'])
@login_required
@manager_authority
def TankSearch():

    addTankForm = AddTankForm()
    modifyTankForm = ModifyTankForm()

    myFilter = request.args.get('filter', '', type=str)
    value = request.args.get('value', '', type=str)

    tankList = None
    if myFilter == "tank":
        if value != "":

            tankList = Tank.query.filter(Tank.tank_name.like('%' + value + '%')).order_by(Tank.tank_name).all()
        else:
            tankList = Tank.query.order_by(Tank.tank_name).all()

    if myFilter == "ip":
        if value != "":
            tankList = Tank.query.filter(Tank.tank_name.like('%' + value + '%')).order_by(Tank.tank_name).all()
        else:
            tankList = Tank.query.order_by(Tank.tank_name).all()

    EventCount = CountEventNow()

    return render_template("tank.html",
                           CountEventNow=EventCount,
                           tankList=tankList,
                           addTankForm=addTankForm,
                           modifyTankForm=modifyTankForm,
                           Action='init',
                           value=value)


def CountEventNow():
    Count = len(EventNow.query.all())
    return Count

