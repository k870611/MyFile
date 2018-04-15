# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from app.models import Server, ServerSdr, ServerLan, ServerFru
from app.permissions import viewer_authorityForAjax


@app.route('/GetServerInfoByAjax', methods=['GET', 'POST'])
@login_required
def GetServerInfoByAjax():
    # now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    mac = request.form.get('mac', '')
    selectedServer = Server.query.filter_by(server_mac=mac).first()

    if selectedServer is None:
        return jsonify({'Success': 'False'})

    situation = {
          '0': 'Power Off',
          '1': 'Power On',
          '2': 'Warning'
        }.get(str(selectedServer.server_status), "Warning")

    serverinfo = {
        'Slot': selectedServer.server_slot,
        'IP': selectedServer.server_ip,
        'MAC': selectedServer.server_mac,
        'Situation': situation,
        "FunctionTag": selectedServer.server_tag,
        "Power": selectedServer.server_power,
        "PowerDetail": selectedServer.server_power_detail.replace('\r\n', '<br/>'),
        "Temp": selectedServer.server_degree,
        "TempDetail": selectedServer.server_degree_detail.replace('\r\n', '<br/>'),
        "hint": selectedServer.server_note.replace('\r\n', '<br/>'),
        "UpdateTime": selectedServer.server_update_time}

    # ------Get SDR Info
    selectedServerSdr = ServerSdr.query.order_by(ServerSdr.server_sdr_name).filter_by(server_id=selectedServer.server_id)

    serverSdr = {}
    i = 0

    for s in selectedServerSdr:
        serverSdr[i] = {
            'name': s.server_sdr_name,
            'status': s.server_sdr_status,
            'value': s.server_sdr_value}
        i += 1

    # ------Get Lan Info
    selectedServerLan = ServerLan.query.order_by(ServerLan.server_lan_name).filter_by(server_id=selectedServer.server_id)

    serverLan = {}
    i = 0

    for s in selectedServerLan:
        serverLan[i] = {'name': s.server_lan_name, 'value': s.server_lan_value}
        i += 1

    # ------Get Fru Info
    selectedServerFru = ServerFru.query.order_by(ServerFru.server_fru_name).filter_by(server_id=selectedServer.server_id)

    serverFru = {}
    i = 0

    for s in selectedServerFru:
        serverFru[i] = {'name': s.server_fru_name, 'value': s.server_fru_value}
        i += 1

    return jsonify({'Success': 'True', 'serverinfo': serverinfo, 'serverSdr': serverSdr, 'serverLan': serverLan, 'serverFru': serverFru})


@app.route('/ChangeFunctionTag', methods=['GET', 'POST'])
@login_required
@viewer_authorityForAjax
def ChangeFunctionTag():

    mac = request.form.get('mac', '')
    text = request.form.get('text', '')
    selectedServer = Server.query.filter_by(server_mac=mac).first()

    selectedServer.server_tag = text
    try:
        db.session.commit()
        app.logger.info("Update " + selectedServer.server_ip + " 's function tag Success")

    except SQLAlchemy.exc.SQLAlchemyError:
        app.logger.exception("Update "+selectedServer.server_ip+" 's function tag Fail")
        return jsonify({'Success': 'False'})

    return jsonify({'Success': 'True'})


@app.route('/ChangeServerNote', methods=['GET', 'POST'])
@login_required
@viewer_authorityForAjax
def ChangeServerNote():

    mac = request.form.get('mac', '')
    text = request.form.get('text', '')
    selectedServer = Server.query.filter_by(server_mac=mac).first()

    selectedServer.server_note = text

    try:
        db.session.commit()
        app.logger.info("Update " + selectedServer.server_ip + " 's not Success")

    except SQLAlchemy.exc.SQLAlchemyError:
        app.logger.exception("Update " + selectedServer.server_ip + " 's note Fail")
        return jsonify({'Success': 'False'})

    return jsonify({'Success': 'True'})



