# -*- coding: utf-8 -*-
from flask import render_template, flash, request, jsonify, url_for, redirect
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from app.models import User, EventNow
from app.forms import AccountCreateForm, AccountModifyForm
from app.permissions import manager_authority

import base64
import sys

# Create Account's JSON Structure (Input)
# [{'account': acc_management_account,
#   'name': acc_management_name,
#   'password': acc_management_password,
#   'organization': acc_management_organization,
#   'email': acc_management_email,
#   'phone': acc_management_phone,
#   'active':accountCreate.active.data,
#   'acc_deadline': acc_management_acc_deadline,
#   'orgManager': acc_management_org_manager}]


@app.route('/accountCreate', methods=['GET', 'POST'])
@login_required
@manager_authority
def accountCreate():

    accountModify = AccountModifyForm()
    accountCreate = AccountCreateForm()

    accountAddSuccess = False
    deadline = ""
    if accountCreate.validate_on_submit():
        if accountCreate.deadlineChk.data is True:
            deadline = accountCreate.deadlineFrom.data+u" ~ "+accountCreate.deadlineTo.data

        user = User(acc_management_account=accountCreate.account.data,
                    acc_management_name=accountCreate.name.data,
                    acc_management_password=accountCreate.password.data,
                    acc_management_organization=accountCreate.organization.data,
                    acc_management_email=accountCreate.email.data,
                    acc_management_phone=accountCreate.cellphone.data,
                    acc_management_active=accountCreate.active.data,
                    acc_management_acc_deadline=deadline,
                    acc_management_org_manager=accountCreate.orgManager.data)

        user.set_password(accountCreate.password.data)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Create Account Success!')
            accountAddSuccess = True
            app.logger.info("Create " + accountCreate.account.data + " account successfully.")

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to Create "+accountCreate.account.data+" account.")

    page = request.args.get('page', 1, type=int)

    rowTotal = len(User.query.all())

    if rowTotal % app.config["DATA_PER_PAGE"] is 0:
        pageTotal = int(rowTotal // app.config["DATA_PER_PAGE"])
    else:
        pageTotal = int(rowTotal // app.config["DATA_PER_PAGE"]) + 1

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

    if accountAddSuccess is not True:
        flash('Sorry, data add fail. Please try again!')

    myFilter = 'account'
    value = ''

    EventCount = CountEventNow()

    return render_template("accmanagement.html",
                           acc_info=users.items,
                           accountCreate=accountCreate,
                           accountModify=accountModify,
                           accountAction='accountCreate',
                           prev_url=prev_url,
                           next_url=next_url,
                           rowTotal=rowTotal,
                           pageTotal=pageTotal,
                           page=page,
                           filter=myFilter,
                           value=value,
                           CountEventNow=EventCount)

# Modify Account's JSON Structure (Input)
# [{'account': u.acc_management_account,
#   'name': u.acc_management_name,
#   'password': u.acc_management_password,
#   'organization': u.acc_management_organization,
#   'email': u.acc_management_email,
#   'phone': u.acc_management_phone,
#   'active': {'True': u'✔', 'False': ''}.get(str(u.acc_management_active), ''),
#   'acc_deadline': u.acc_management_acc_deadline}]


@app.route('/accountModify', methods=['GET', 'POST'])
@login_required
@manager_authority
def accountModify():

    accountCreate = AccountCreateForm()
    accountModify = AccountModifyForm()

    accountModifySuccess = False
    deadline = ""

    if accountModify.validate_on_submit():
        if accountCreate.deadlineChk.data is True:
            deadline = accountCreate.deadlineFrom.data + u" ~ " + accountCreate.deadlineTo.data

        user = User.query.filter_by(acc_management_account=accountModify.originalAccount.data).first()

        user.acc_management_account = accountModify.account.data
        user.acc_management_name = accountModify.name.data
        user.set_password(accountCreate.password.data)
        user.acc_management_organization = accountModify.organization.data
        user.acc_management_email = accountModify.email.data
        user.acc_management_phone = accountModify.cellphone.data
        user.acc_management_active = accountModify.active.data
        user.acc_management_acc_deadline = deadline

        try:
            db.session.commit()
            flash('Account was Update!')
            accountModifySuccess = True
            app.logger.info("Modify " + accountCreate.account.data + " account successfully.")

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to modify " + accountCreate.account.data + " account.")

    page = request.args.get('page', 1, type=int)

    rowTotal = len(User.query.all())

    if rowTotal % app.config["DATA_PER_PAGE"] is 0:
        pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"])
    else:
        pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"]) + 1

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

    if accountModifySuccess is not True:
        flash('Sorry, modify fail. Please try again!')

    myFilter = 'account'

    EventCount = CountEventNow()

    return render_template("accmanagement.html",
                           acc_info=users.items,
                           accountCreate=accountCreate,
                           accountModify=accountModify,
                           accountAction='accountModify',
                           prev_url=prev_url,
                           next_url=next_url,
                           rowTotal=rowTotal,
                           pageTotal=pageTotal,
                           page=page,
                           filter=myFilter,
                           value='',
                           CountEventNow=EventCount)


# Delete Account's JSON Structure (Output)
# [{'account': account,
#   'deleteInfo': deleteInfo}]

@app.route('/accountDelete', methods=['GET', 'POST'])
@login_required
@manager_authority
def accountDelete():
    deleteInfo = ''
    account = request.form.get('account', '')

    user = User.query.filter_by(acc_management_account=account).first()

    if user.acc_management_account is not current_user.acc_management_account:
        try:
            db.session.delete(user)
            db.session.commit()
            app.logger.info("Delete " + user.acc_management_account + " account successfully.")

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to delete " + user.acc_management_account + " account.")

    else:
        deleteInfo = 'You cannot delete yourself !!!'

    return jsonify({'account': account, 'deleteInfo': deleteInfo})


# Get Resolute Account's JSON Structure (Output)
# [{'account': User.acc_management_account,
#   'name': User.acc_management_name,
#   'password': User.acc_management_password,
#   'organization': User.acc_management_organization,
#   'email': User.acc_management_email,
#   'phone': User.acc_management_phone,
#   'active': {'True': u'✔', 'False': ''}.get(str(User.acc_management_active), ''),
#   'acc_deadline': User.acc_management_acc_deadline,
#   'orgManager': User.acc_management_org_manager}]


@app.route('/accountSearch', methods=['GET', 'POST'])
@login_required
@manager_authority
def accountSearch():
    page = request.args.get('page', 1, type=int)
    click = request.args.get('click', '')

    myFilter = request.args.get('filter', '', type=str)
    value = request.args.get('value', '', type=str)

    users = None

    if myFilter == "account":
        if value != "":
            users = User.query.filter(User.acc_management_account.like('%' + value + '%'))\
                .order_by(User.acc_management_account)

    elif myFilter == "name":
        if value != "":
            users = User.query.filter(User.acc_management_name.like('%' + value + '%'))\
                .order_by(User.acc_management_account)

    elif myFilter == "org":
        if value != "":
            users = User.query.filter(User.acc_management_organization.like('%'+value+'%'))\
                .order_by(User.acc_management_account)

    if users is not None:
        rowTotal = len([u for u in users])

        if rowTotal % app.config["DATA_PER_PAGE"] is 0:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"])
        else:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"]) + 1

        if click == 'b':
            page = 1
        elif click == 'e':
            page = pageTotal

        users = users.paginate(page, app.config["DATA_PER_PAGE"], False)

    else:
        rowTotal = len(User.query.all())

        if rowTotal % app.config["DATA_PER_PAGE"] is 0:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"])
        else:
            pageTotal = int(rowTotal / app.config["DATA_PER_PAGE"]) + 1

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

    prev_url = url_for('accountSearch', page=users.prev_num, filter=myFilter, value=value) if users.has_prev else None
    next_url = url_for('accountSearch', page=users.next_num, filter=myFilter, value=value) if users.has_next else None

    accountCreate = AccountCreateForm()
    accountModify = AccountModifyForm()

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
                           value=value,
                           CountEventNow=EventCount)


def CountEventNow():
    Count = len(EventNow.query.all())
    return Count
