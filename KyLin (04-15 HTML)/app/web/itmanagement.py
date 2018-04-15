from flask import render_template, request, jsonify, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from app.permissions import manager_authority
from app.models import Server, EventNow
from datetime import datetime

import base64
import sys


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
    server.server_update_time = now

    server.set_password(password)

    try:
        db.session.commit()
        app.logger.info("Modify server" + server.server_ip + " IPMI successfully.")

    except SQLAlchemy.exc.SQLAlchemyError:
        app.logger.exception("Fail to Modify " + server.server_ip + ".")

    return jsonify({'Success': 'True'})


@app.route('/IpmiDelete', methods=['GET', 'POST'])
@login_required
@manager_authority
def IpmiDelete():
    mac = request.form.get('mac', '')

    server = Server.query.filter_by(server_mac=mac).first()

    if server is None:
        return jsonify({'Success': 'False'})

    try:
        db.session.delete(server)
        db.session.commit()

        app.logger.info("Delete server" + server.server_ip + " IPMI successfully.")

    except SQLAlchemy.exc.SQLAlchemyError:
        app.logger.exception("Fail to Delete " + server.server_ip + ".")

    return jsonify({'Success': 'True'})


@app.route('/IpmiSearch', methods=['GET', 'POST'])
@login_required
@manager_authority
def IpmiSearch():
    page = request.args.get('page', 1, type=int)
    click = request.args.get('click', '')

    select = request.args.get('select', '')
    value = request.args.get('text', '')

    server = None

    if select == "ip":
        if value != "":
            server = Server.query.filter(Server.server_ip.like('%' + value + '%')) \
                .order_by(Server.server_slot)

    elif select == "mac":
        if value != "":
            server = Server.query.filter(Server.server_mac.like('%' + value + '%')) \
                .order_by(Server.server_slot)

    if server is not None:
        rowTotal = len([s for s in server])

        if rowTotal % app.config["DATA_PER_PAGE"] is 0:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"])
        else:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"]) + 1

        if click == 'b':
            page = 1
        elif click == 'e':
            page = pageTotal

        server = server.paginate(page, app.config["DATA_PER_PAGE"], False)

    else:
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
        if float(sys.version[:3]) < 3:
            s.decodePwd = base64.b64decode(s.server_password.encode('utf-8'))

        else:
            s.decodePwd = str(base64.b64decode(s.server_password.encode('utf-8')), 'utf-8')
        i += 1

    prev_url = url_for('IpmiSearch', page=server.prev_num, select=select, text=value) if server.has_prev else None
    next_url = url_for('IpmiSearch', page=server.next_num, select=select, text=value) if server.has_next else None

    EventCount = CountEventNow()
    return render_template("itmanagement.html", CountEventNow=EventCount, server_list=server.items,
                           prev_url=prev_url,
                           next_url=next_url,
                           rowTotal=rowTotal,
                           pageTotal=pageTotal,
                           page=page,
                           select=select,
                           value=value, )


def CountEventNow():
    Count = len(EventNow.query.all())
    return Count
