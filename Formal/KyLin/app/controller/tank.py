from flask import render_template, flash, request, jsonify
from flask_login import login_required
import sqlalchemy

from app import app, db
from app.models import Tank, Server, ServerDetail, ServerSdr, ServerLan, ServerFru
from app.forms import AddTankForm, ModifyTankForm


import os
import subprocess
from datetime import datetime


def arp_check(ip):
    cmd = "ARP -a " + ip
    s = subprocess.check_output(cmd)

    a = str(s.decode('GB2312').split('\r\n')[-2])

    mystr = ""
    ary = set()

    for b in a:
        if b == ' ':
            spaceChk = True

            if mystr != '':
                ary.add(mystr)
                mystr = ''
        else:
            spaceChk = False

        if not spaceChk:
            mystr += b
            spaceChk = False

    for a in ary:
        if a.lower() == 'arp':
            return False

    return True


@app.route('/AddTank', methods=['GET', 'POST'])
def AddTank():

    addTankForm = AddTankForm()
    modifyTankForm = ModifyTankForm()
    tankAddSuccess = False
    tank_num_error = False

    tank_num = len(Tank.query.all())

    if tank_num >= 16:
        tank_num_error = True

    if addTankForm.validate_on_submit() and not tank_num_error:

        tank = Tank(tank_name=addTankForm.name.data, tank_description=addTankForm.description.data)

        try:
            db.session.add(tank)
            db.session.commit()
            flash('Create Tank Success!')
            app.logger.info("Create " + addTankForm.name.data + " tank successfully.")

            tankAddSuccess = True

        except sqlalchemy.exc.DatabaseError:
            db.session.rollback()
            app.logger.exception("Fail to create " + addTankForm.name.data + " tank.")

    tankList = Tank.query.order_by(Tank.tank_name).all()
    EventCount = CountEventNow()

    if tank_num_error:
        flash('Sorry, Tank number cannot over 16!')

        return render_template("tank.html",
                               CountEventNow=EventCount,
                               tankList=tankList,
                               addTankForm=addTankForm,
                               modifyTankForm=modifyTankForm,
                               Action='create',
                               value='')

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

        except sqlalchemy.exc.DatabaseError:
            db.session.rollback()
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
def DeleteTank():

    t = request.form.get('tank', '')
    tank = Tank.query.filter_by(tank_name=t).first()

    try:
        servers = Server.query.filter_by(tank_id=tank.id).all()
        for s in servers:

            s.server_slot = 0
            s.server_ip = ''
            s.server_mac = ''
            s.server_account = ''
            s.server_password = ''
            s.tank_id = None

            detail = ServerDetail.query.filter_by(server_id=s.id).first()
            detail.server_tag = ''
            detail.server_note = ''

            db.session.commit()

    except sqlalchemy.exc.DatabaseError:
        db.session.rollback()
        app.logger.exception("Fail to delete " + tank.tank_name + " tank.")

    try:
        db.session.delete(tank)
        db.session.commit()

        app.logger.info("Delete " + tank.tank_name + " tank successfully.")
        deleteInfo = 'true'

    except sqlalchemy.exc.DatabaseError:
        db.session.rollback()
        app.logger.exception("Fail to delete " + tank.tank_name + " tank.")

    return jsonify({'tank': t, 'deleteInfo': deleteInfo})


@app.route('/GetServerByAjax', methods=['GET', 'POST'])
def GetServerByAjax():
    page = request.args.get('page', 1, type=int)
    tank = request.args.get('tank', '')

    select = request.args.get('select', '')
    text = request.args.get('text', '')

    if select == 'ip':
        server = Server.query.join(Tank).filter(Server.server_ip.like('%'+text+'%'), Tank.tank_name.like('%'+tank+'%'))\
            .order_by(Server.server_slot)

    elif select == 'mac':
        server = Server.query.join(Tank).filter(Server.server_mac.like('%'+text+'%'), Tank.tank_name.like('%'+tank+'%'))\
            .order_by(Server.server_slot)

    else:
        server = Server.query.join(Tank).filter(Tank.tank_name.like('%'+tank+'%')).order_by(Server.server_slot)

    if server is None:
        return jsonify({'Success': 'False'})

    rowCount = len([u for u in server])

    if rowCount % app.config["DATA_PER_PAGE"] is 0:
        totalPage = int(rowCount // app.config["DATA_PER_PAGE"])
    else:
        totalPage = int(rowCount / app.config["DATA_PER_PAGE"]) + 1

    server = server.paginate(page, app.config["DATA_PER_PAGE"], False)

    serverInfo = {}

    tag = ''
    note = ''
    i = 0
    for u in server.items:
        pwd = u.server_password
        detail = ServerDetail.query.filter_by(server_id=u.id).first()

        if detail is not None:
            tag = detail.server_tag
            note = detail.server_note

        serverInfo[i] = {
            'id': u.id,
            'slot': u.server_slot,
            'ip': u.server_ip,
            'mac': u.server_mac,
            'tag': tag,
            'acc': u.server_account,
            'pwd': pwd,
            'note': note,
            'active': u.server_active}
        i += 1

    return jsonify({'Success': 'True', 'userInfo': serverInfo, 'totalPage': totalPage, 'totalRow': rowCount, 'page': page})


@app.route('/GetAddServerIntoTankInfo', methods=['GET', 'POST'])
def GetAddServerIntoTankInfo():
    tank = request.form.get('tank', "")
    start_ip = request.form.get('startIp', "")
    end_ip = request.form.get('endIp', "")
    account = request.form.get('account', '')
    pwd = request.form.get('password', '')

    my_tank = Tank.query.filter_by(tank_name=tank).first()
    tank_id = my_tank.id

    if end_ip == '':

        chk = arp_check(start_ip)

        if not chk:
            return jsonify({'info': 'success', 'server_list': {}})

        server_tank = Server.query.filter(Server.tank_id == tank_id).order_by(Server.server_slot.desc()).first()

        if server_tank is None:
            slot = 1
        else:
            slot = int(server_tank.server_slot)+1

        if slot >= 36:
            return jsonify({'info': 'success', 'server_list': {}})

        server = Server.query.filter(Server.server_ip == start_ip).first()

        if server is None:
            server = Server.query.filter(Server.server_ip == '', Server.server_mac == '').first()

        else:
            return jsonify({'info': 'success', 'server_list': {}})

        server_list = {}

        i = 0

        tag = ''
        selectServerDetail = ServerDetail.query.filter_by(server_id=server.id).first()

        if selectServerDetail is not None:
            tag = selectServerDetail.server_tag

        server_list[i] = {
            'id': server.id,
            'slot': slot,
            'ip': start_ip,
            'account': account,
            'password': pwd,
            'tag': tag,
            'mac': '',
            'connect': 'N/A'}
        i += 1

        return jsonify({'info': 'success', 'server_list': server_list})

    elif end_ip == 'mac':
        mac_address = str(start_ip).split('\n')
        mac_ary = []

        for m in mac_address:
            if m not in mac_ary:
                mac_ary.append(m)
            if len(mac_ary) > 36:
                break

        server_list = {}
        i = 0

        server_tank = Server.query.filter(Server.tank_id == tank_id).order_by(Server.server_slot.desc()).first()

        if server_tank is None:
            slot = 1
        else:
            slot = int(server_tank.server_slot) + 1

        if slot >= 36:
            return jsonify({'info': 'success', 'server_list': {}})

        empty_count = 0

        for m in mac_ary:

            server = Server.query.filter(Server.server_mac == m).group_by(Server.server_mac).first()

            if server is None:
                empty_server = Server.query.filter(Server.server_ip == '', Server.server_mac == '').all()

                server = empty_server[empty_count]
                empty_count += 1

            else:
                continue

            tag = ''
            selectServerDetail = ServerDetail.query.filter_by(server_id=server.id).first()

            if selectServerDetail is not None:
                tag = selectServerDetail.server_tag

            server_list[i] = {
                'id': server.id,
                'slot': slot,
                'ip': server.server_ip,
                'account': account,
                'password': pwd,
                'tag': tag,
                'mac': m,
                'connect': 'N/A'}

            slot += 1
            i += 1
            
            if slot > 36:
                return jsonify({'info': 'success', 'server_list': server_list})

        return jsonify({'info': 'success', 'server_list': server_list})

    else:
        ip_start_ary = str(start_ip).split('.')
        ip_end_ary = str(end_ip).split('.')

        ip_range_start = ip_start_ary[3]
        ip_range_end = ip_end_ary[3]

        server_list = {}
        i = 0

        server_tank = Server.query.filter(Server.tank_id == tank_id).order_by(Server.server_slot.desc()).first()

        if server_tank is None:
            slot = 1
        else:
            slot = int(server_tank.server_slot) + 1

        if slot >= 36:
            return jsonify({'info': 'success', 'server_list': {}})

        empty_count = 0

        for idx in range(int(ip_range_end) - int(ip_range_start)+1):
            ip_last = (int(idx)+int(ip_range_start))
            ip = ip_start_ary[0]+'.'+ip_start_ary[1]+'.'+ip_start_ary[2]+'.'+str(ip_last)

            chk = arp_check(ip)

            if not chk:
                continue

            server = Server.query.filter(Server.server_ip == ip).group_by(Server.server_ip).first()

            if server is None:
                empty_server = Server.query.filter(Server.server_ip == '', Server.server_mac == '').all()

                server = empty_server[empty_count]
                empty_count += 1

            else:
                continue

            tag = ''
            selectServerDetail = ServerDetail.query.filter_by(server_id=server.id).first()

            if selectServerDetail is not None:
                tag = selectServerDetail.server_tag

            server_list[i] = {
                'id': server.id,
                'slot': slot,
                'ip': ip,
                'account': account,
                'password': pwd,
                'tag': tag,
                'mac': server.server_mac,
                'connect': 'N/A'}
            slot += 1

            if slot > 36:
                return jsonify({'info': 'success', 'server_list': server_list})

            i += 1

        return jsonify({'info': 'success', 'server_list': server_list})


@app.route('/AddServer', methods=['GET', 'POST'])
def AddServer():

    tank = request.get_json(force=True).get('tank')
    servers = request.get_json(force=True).get('servers')

    my_tank = Tank.query.filter_by(tank_name=tank).first()
    tank_id = my_tank.id

    if servers is None or not servers:
        return jsonify({'Success': 'False'})

    for s in servers:

        server = Server.query.filter(Server.id == s[7]).first()
        server_detail = ServerDetail.query.filter(ServerDetail.server_id == s[7]).first()

        if server_detail is not None:
            server.server_slot = s[0]
            server.server_ip = s[1]
            server.server_account = s[2]
            server.server_password = s[3]
            server_detail.server_tag = s[4]
            server_detail.server_note = ''
            server.server_mac = s[5]
            server.tank_id = tank_id
            server.server_active = False

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            server.server_update_time = now

            try:
                db.session.commit()
                app.logger.info("Add IPMI" + server.server_ip + " into " + tank + " successfully.")

            except sqlalchemy.exc.DatabaseError:
                db.session.rollback()
                app.logger.exception("Fail to Add IPMI" + server.server_ip + " into " + tank + ".")

        else:
            server.server_slot = s[0]
            server.server_ip = s[1]
            server.server_account = s[2]
            server.server_password = s[3]
            server.server_mac = s[5]
            server.tank_id = tank_id
            server.server_active = False
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            server.server_update_time = now

            try:
                db.session.commit()

                detail = ServerDetail(server_tag=s[4], server_id=s[7], server_note='')
                db.session.add(detail)
                db.session.commit()

                app.logger.info("Add IPMI" + server.server_ip + " into " + tank + " successfully.")

            except sqlalchemy.exc.DatabaseError:
                db.session.rollback()
                app.logger.exception("Fail to Add IPMI" + server.server_ip + " into " + tank + ".")

    return jsonify({'Success': 'True'})


@app.route('/IpmiModify', methods=['GET', 'POST'])
def IpmiModify():
    slot = request.form.get('slot', '')
    ip = request.form.get('ip', '')
    account = request.form.get('account', '')
    password = request.form.get('password', '')
    mac = request.form.get('mac', '')
    tag = request.form.get('tag', '')
    memo = request.form.get('memo', '')
    orgMac = request.form.get('orgMac', '')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    server = Server.query.filter_by(server_slot=slot, server_mac=orgMac).first()

    server_check = Server.query.filter_by(server_mac=mac).first()

    if server_check is not None:
        if server.id != server_check.id:
            return jsonify({'info': 'fail', 'Success': 'This Mac already exist in this or other tank'})

    server_check = Server.query.filter_by(server_ip=ip).first()

    if server_check is not None:
        if server.id != server_check.id:
            return jsonify({'info': 'fail', 'Success': 'This IP already exist in this or other tank'})

    if server is None:
        return jsonify({'Success': 'False'})

    try:
        server.server_slot = slot
        server.server_ip = ip
        server.server_account = account
        server.server_mac = mac
        server.server_active = False
        server.server_update_time = now
        server.set_password(password)

        db.session.commit()

        selectServerDetail = ServerDetail.query.filter_by(server_id=server.id).first()
        selectServerDetail.server_note = memo
        selectServerDetail.server_tag = tag

        db.session.commit()

        app.logger.info("Modify server" + server.server_ip + " IPMI successfully.")

    except sqlalchemy.exc.DatabaseError:
        db.session.rollback()
        app.logger.exception("Fail to Modify " + server.server_ip + ".")

    return jsonify({'Success': 'True'})


@app.route('/DelServerFromTank', methods=['GET', 'POST'])
def DelServerFromTank():

    tank_name = request.get_json(force=True).get('tank_name')
    acc = request.get_json(force=True).get('acc')

    for i in acc:
        if i == '' or i is None:
            continue

        server = Server.query.filter_by(id=i).first()
        server_id = server.id
        if server is None:
            continue

        try:
            sdr = ServerSdr.query.order_by(ServerSdr.insert_time.desc()).filter_by(server_id=server_id).all()

            if sdr is not None:
                for s in sdr:
                    db.session.delete(s)
                    db.session.commit()

            lan = ServerLan.query.order_by(ServerLan.insert_time.desc()).filter_by(server_id=server_id).all()

            if lan is not None:
                for l in lan:
                    db.session.delete(l)
                    db.session.commit()

            fru = ServerFru.query.order_by(ServerFru.insert_time.desc()).filter_by(server_id=server_id).all()

            if fru is not None:
                for f in fru:
                    db.session.delete(f)
                    db.session.commit()

            detail = ServerDetail.query.filter_by(server_id=server_id).all()

            if detail is not None:
                for f in detail:
                    f.server_tag = ''
                    f.server_note = ''
                    f.server_status = None
                    f.server_type = ''

                    db.session.commit()

            server.server_ip = ''
            server.server_mac = ''
            server.server_update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            server.server_account = ''
            server.server_password = ''
            server.server_active = 0

            db.session.commit()

            app.logger.info("Delete server " + server.server_mac + " from tank " + tank_name + ".")

        except sqlalchemy.exc.DatabaseError:
            db.session.rollback()
            app.logger.exception("Fail to delete server " + server.server_mac + " from role " + tank_name + ".")
            return jsonify({'Success': 'Fail'})

    return jsonify({'Success': 'True'})


@app.route('/TankSearch', methods=['GET', 'POST'])
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


@app.route('/ipmiRestart', methods=['GET', 'POST'])
def ipmiRestart():
    tank_name = request.get_json(force=True).get('tank_name')
    acc = request.get_json(force=True).get('acc')

    tank = Tank.query.filter_by(tank_name=tank_name).first()
    tank_id = tank.id

    for i in acc:
        if i == '' or i is None:
            continue

        server = Server.query.filter_by(id=i, tank_id=tank_id).first()

        if server is None:
            return jsonify({'Success': 'fail'})

        ip = server.server_ip
        account = server.server_account
        password = server.server_password

        os.environ['IPMI_PASSWORD'] = password

        cmd = '..\\tools\\ipmitool -H {} -U {} -E mc reset cold'.format(ip, account)

        try:
            success = subprocess.check_output(cmd)

        except subprocess.CalledProcessError as grepexc:
            success = int(-1)

        if success == int(-1):
            return jsonify({'info': 'Fail'})

        else:
            return jsonify({'info': 'Success'})

    return jsonify({'Success': 'True'})


@app.route('/btnModifyTest', methods=['GET', 'POST'])
def btnModifyTest():

    ip = request.form.get('ip', '')
    account = request.form.get('account', '')
    password = request.form.get('password', '')

    os.environ['IPMI_PASSWORD'] = password

    cmd = '..\\tools\\ipmitool -H {} -U {} -E mc selftest'.format(ip, account)

    try:
        success = subprocess.check_output(cmd)

    except subprocess.CalledProcessError as grepexc:
        success = grepexc.output
        info = success.decode('UTF-8')

        if info == "":
            info = 'selfTest Fail'

        return jsonify({'success': 'fail', 'info': info})

    return jsonify({'success': 'true', 'info': success.decode('UTF-8')})


def CountEventNow():
    Count = 0
    return Count

