# -*- coding: utf-8 -*-
from flask import render_template

from app.models import *
from app import app
from app.forms import AddTankForm, ModifyTankForm


@app.route('/')
@app.route('/tankManagement')
def tankManagement():

    addTankForm = AddTankForm()
    modifyTankForm = ModifyTankForm()
    tankList = Tank.query.order_by(Tank.tank_name).all()
    EventCount = 0

    return render_template("tank.html",
                           CountEventNow=EventCount,
                           tankList=tankList,
                           addTankForm=addTankForm,
                           modifyTankForm=modifyTankForm,
                           Action='init',
                           value='')

