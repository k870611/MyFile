# -*- coding: utf-8 -*-
from flask import url_for, request, render_template
from flask_login import login_required

from app import app
from app.models import Log, EventNow, User
from app.permissions import manager_authority

from datetime import datetime
import re


@app.route('/logSearch', methods=['GET', 'POST'])
@login_required
@manager_authority
def logSearch():
    page = request.args.get('page', 1, type=int)
    click = request.args.get('click', '')

    org = request.args.get('org', '', type=str)
    module = request.args.get('module', '', type=str)
    level = request.args.get('level', '', type=str)
    account = request.args.get('account', '', type=str)
    description = request.args.get('description', '', type=str)
    source = re.sub('\s', '', request.args.get('source', '', type=str))
    since = request.args.get('since', '1900-01-01', type=str)
    sinceTime = request.args.get('sinceTime', '00:00', type=str)
    until = request.args.get('until', '3000-12-31', type=str)
    untilTime = request.args.get('untilTime', '00:00', type=str)

    dateFrom = datetime.strptime('{} {}'.format(since, sinceTime), '%Y-%m-%d %H:%M')
    dateTo = datetime.strptime('{} {}'.format(until, untilTime), '%Y-%m-%d %H:%M')

    arySearch = [org, module, level, account, description, source, since, sinceTime, until, untilTime]

    logs = Log.query.filter(Log.log_user_org.like('%' + org + '%'),
                            Log.log_module.like('%' + module + '%'),
                            Log.log_level.like('%' + level + '%'),
                            Log.log_user_account.like('%' + account + '%'),
                            Log.log_description.like('%' + description + '%'),
                            Log.log_source.like('%' + source + '%'),
                            Log.log_date >= dateFrom,
                            Log.log_date <= dateTo).order_by(Log.log_date.desc())

    if logs is not None:
        rowTotal = len([u for u in logs])

        if rowTotal % app.config["DATA_PER_PAGE"] is 0:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"])
        else:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"]) + 1

        if click == 'b':
            page = 1
        elif click == 'e':
            page = pageTotal

        logs = logs.paginate(page, app.config["DATA_PER_PAGE"], False)

    else:
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

    prev_url = url_for('logSearch',
                       page=logs.prev_num,
                       org=org,
                       module=module,
                       level=level,
                       account=account,
                       description=description,
                       source=source,
                       since=since,
                       sinceTime=sinceTime,
                       until=until,
                       untilTime=untilTime) if logs.has_prev else None

    next_url = url_for('logSearch',
                       page=logs.next_num,
                       org=org,
                       module=module,
                       level=level,
                       account=account,
                       description=description,
                       source=source,
                       since=since,
                       sinceTime=sinceTime,
                       until=until,
                       untilTime=untilTime) if logs.has_next else None

    EventCount = CountEventNow()
    return render_template("log.html", CountEventNow=EventCount, log_list=logs.items,
                           prev_url=prev_url,
                           next_url=next_url,
                           rowTotal=rowTotal,
                           pageTotal=pageTotal,
                           page=page,
                           arySearch=arySearch)


def CountEventNow():
    Count = len(EventNow.query.all())
    return Count

