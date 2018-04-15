from flask import render_template, flash, request, jsonify
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from app.permissions import manager_authority
from app.models import Role, User, EventNow
from app.forms import RoleModifyForm


@app.route('/roleModify', methods=['GET', 'POST'])
@login_required
@manager_authority
def roleModify():

    roleModifyForm = RoleModifyForm()
    roleModifySuccess = False

    if roleModifyForm.validate_on_submit():

        role = Role.query.filter_by(role_name=roleModifyForm.originalRole.data).first()
        role.role_name = roleModifyForm.name.data
        role.role_description = roleModifyForm.description.data

        try:
            db.session.commit()
            flash('Modify role success!')
            app.logger.info("modify " + roleModifyForm.originalRole.data + " role successfully.")

            roleModifySuccess = True

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to modify " + roleModifyForm.originalRole.data + " role.")

    roleList = Role.query.order_by(Role.role_name).all()
    EventCount = CountEventNow()

    if roleModifySuccess is not True:
        flash('Sorry, modify fail. Please try again!')

    return render_template("role.html",
                           CountEventNow=EventCount,
                           roleList=roleList,
                           roleModifyForm=roleModifyForm,
                           Action='modify',
                           value='')


@app.route('/RoleSearch', methods=['GET', 'POST'])
@login_required
@manager_authority
def RoleSearch():
    roleModifyForm = RoleModifyForm()

    myFilter = request.args.get('filter', '', type=str)
    value = request.args.get('value', '', type=str)

    roleList = None
    if myFilter == "role":
        if value != "":
            roleList = Role.query.filter(Role.role_name.like('%' + value + '%')).order_by(Role.role_name)
        else:
            roleList = Role.query.order_by(Role.role_name).all()

    EventCount = CountEventNow()

    return render_template("role.html",
                           CountEventNow=EventCount,
                           roleList=roleList,
                           roleModifyForm=roleModifyForm,
                           Action='init',
                           value=value)


@app.route('/GetRoleAccByAjax', methods=['GET', 'POST'])
@login_required
@manager_authority
def GetRoleAccByAjax():
    page = request.args.get('page', 1, type=int)
    auth = request.args.get('auth', '')

    select = request.args.get('select', '')
    text = request.args.get('text', '')

    if select == 'acc':
        users = User.query.filter(User.role_id == auth, User.acc_management_account.like('%' + text + '%'))

    elif select == 'name':
        users = User.query.filter(User.role_id == auth, User.acc_management_name.like('%' + text + '%'))

    else:
        users = User.query.filter(User.role_id == auth)

    if users is None:
        return jsonify({'Success': 'False'})

    rowCount = len([u for u in users])

    if rowCount % app.config["DATA_PER_PAGE"] is 0:
        totalPage = int(rowCount // app.config["DATA_PER_PAGE"])
    else:
        totalPage = int(rowCount / app.config["DATA_PER_PAGE"]) + 1

    users = users.paginate(page, app.config["DATA_PER_PAGE"], False)

    userInfo = {}
    i = 0
    for u in users.items:
        userInfo[i] = {
            'account': u.acc_management_account,
            'name': u.acc_management_name}
        i += 1

    return jsonify({'Success': 'True', 'userInfo': userInfo, 'totalPage': totalPage, 'totalRow': rowCount, 'page': page})


@app.route('/GetAccNotInRoleByAjax', methods=['GET', 'POST'])
@login_required
@manager_authority
def GetAccNotInRoleByAjax():
    page = request.args.get('page', 1, type=int)
    auth = request.args.get('auth', '')
    select = request.args.get('select', '')
    text = request.args.get('text', '')

    if select == 'acc':
        users = User.query.filter(User.role_id != auth, User.acc_management_account.like('%' + text + '%'))

    elif select == 'name':
        users = User.query.filter(User.role_id != auth, User.acc_management_name.like('%' + text + '%'))

    else:
        users = User.query.filter(User.role_id != auth)

    if users is None:
        return jsonify({'Success': 'False'})

    rowCount = len([u for u in users])

    if rowCount % app.config["DATA_PER_PAGE"] is 0:
        totalPage = int(rowCount // app.config["DATA_PER_PAGE"])
    else:
        totalPage = int(rowCount // app.config["DATA_PER_PAGE"]) + 1

    users = users.paginate(page, app.config["DATA_PER_PAGE"], False)

    userInfo = {}
    i = 0
    for u in users.items:
        userInfo[i] = {
            'account': u.acc_management_account,
            'name': u.acc_management_name}
        i += 1

    return jsonify({'Success': 'True', 'userInfo': userInfo, 'totalPage': totalPage, 'totalRow': rowCount, 'page': page})


@app.route('/AddAccIntoRole', methods=['GET', 'POST'])
@login_required
@manager_authority
def AddAccIntoRole():
    acc = request.get_json(force=True).get('acc')
    auth = request.get_json(force=True).get('auth')
    CantChangeYourself = 'False'

    if auth is None or auth == '':
        return jsonify({'Success': 'False'})

    for i in acc:
        if i == '' or i is None:
            continue

        user = User.query.filter_by(acc_management_account=i).first()
        role = Role.query.filter_by(role_auth=auth).first()
        if user is None or user == current_user:
            if user == current_user:
                CantChangeYourself = 'True'
            continue

        user.role_id = auth

        try:
            db.session.commit()
            app.logger.info("Add account " + user.acc_management_account + " into role "+role.role_name+".")

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to add account "+user.acc_management_account+" into role "+role.role_name+".")

    return jsonify({'Success': 'True', 'CantChangeYourself': CantChangeYourself})


@app.route('/DelRoleAcc', methods=['GET', 'POST'])
@login_required
@manager_authority
def DelRoleAcc():
    acc = request.get_json(force=True).get('acc')
    role = (Role.query.filter_by(role_auth=3).first())
    CantChangeYourself = 'False'

    for i in acc:
        if i == '' or i is None:
            continue

        user = User.query.filter_by(acc_management_account=i).first()
        originalRole = (Role.query.filter_by(role_id=user.role_id).first()).role_name
        print(originalRole)

        if user is None or user == current_user:
            if user == current_user:
                CantChangeYourself = 'True'
            continue

        user.role_id = role.role_id

        try:
            db.session.commit()
            app.logger.info("Delete account " + user.acc_management_account + " from role " + originalRole + ".")

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to delete account "+user.acc_management_account+" from role "+originalRole+".")

    return jsonify({'Success': 'True', 'CantChangeYourself': CantChangeYourself})


@app.route('/ChangeViewByAjax', methods=['GET', 'POST'])
@login_required
@manager_authority
def ChangeViewByAjax():

    server = {'true': True, 'false': False}.get(str(request.form.get('server', '')), True)
    event = {'true': True, 'false': False}.get(str(request.form.get('event', '')), True)
    auth = request.form.get('auth', '')

    role = Role.query.filter_by(role_auth=auth).first()

    if role is not None:
        role.role_server = server
        role.role_event = event

        try:
            db.session.commit()
            app.logger.info("Change Role " + role.role_name + " 's view permission.")

            return jsonify({'Success': 'True'})

        except SQLAlchemy.exc.SQLAlchemyError:
            app.logger.exception("Fail to change Role " + role.role_name + " 's view permission.")

    else:
        return jsonify({'Success': 'False'})


def CountEventNow():
    Count = len(EventNow.query.all())
    return Count

