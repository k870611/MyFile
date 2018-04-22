# -*- coding: utf-8 -*-
from flask import render_template, request, url_for
from flask_login import login_required

from app import app, db
from app.models import User, EventNow
from app.permissions import manager_authority

from datetime import datetime
import datetime as date


@app.route('/onlineSearch', methods=['GET', 'POST'])
@login_required
@manager_authority
def onlineSearch():
    page = request.args.get('page', 1, type=int)
    myFilter = request.args.get('filter', '', type=str)
    value = request.args.get('value', '', type=str)

    deadline = datetime.now() + date.timedelta(minutes=-30)

    users = None

    if myFilter == "account":
        if value != "":
            users = User.query.filter(User.acc_management_operate_date > deadline,
                                      User.acc_management_account.like('%' + value + '%')).order_by(User.acc_management_account)

    elif myFilter == "name":
        if value != "":
            users = User.query.filter(User.acc_management_operate_date > deadline,
                                      User.acc_management_name.like('%' + value + '%')).order_by(User.acc_management_account)

    elif myFilter == "org":
        if value != "":
            users = User.query.filter(User.acc_management_operate_date > deadline,
                                      User.acc_management_organization.like('%' + value + '%')).order_by(User.acc_management_account)

    if users is not None:
        rowTotal = len([u for u in users])

        if rowTotal % app.config["DATA_PER_PAGE"] is 0:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"])
        else:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"]) + 1

        users = users.paginate(page, app.config["DATA_PER_PAGE"], False)

    else:
        users = User.query.filter(User.acc_management_operate_date > deadline).order_by(User.acc_management_operate_date.desc())
        rowTotal = len([u for u in users])

        if rowTotal % app.config["DATA_PER_PAGE"] is 0:
            pageTotal = int(rowTotal // app.config["DATA_PER_PAGE"])
        else:
            pageTotal = int(rowTotal // app.config["DATA_PER_PAGE"]) + 1

        users = users.paginate(page, app.config["DATA_PER_PAGE"], False)

    prev_url = url_for('onlineSearch', page=users.prev_num, filter=myFilter, value=value) if users.has_prev else None
    next_url = url_for('onlineSearch', page=users.next_num, filter=myFilter, value=value) if users.has_next else None

    EventCount = CountEventNow()
    return render_template("OnlineUser.html",
                           acc_info=users.items,
                           prev_url=prev_url,
                           next_url=next_url,
                           rowTotal=rowTotal,
                           pageTotal=pageTotal,
                           page=page,
                           filter=myFilter,
                           value=value,
                           CountEventNow=EventCount)


def CountEventNow():
    Count = len(EventNow.query.all())
    return Count
