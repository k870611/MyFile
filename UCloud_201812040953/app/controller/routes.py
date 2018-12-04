# -*- coding: utf-8 -*-
from flask import render_template

from app.models import *
from app import app
from app.forms import BiosConfigForm


@app.route('/tankManagement')
def tankManagement():
    tankList = Tank.query.order_by(Tank.tank_name).all()

    return render_template("tank.html",
                           CountEventNow=0,
                           tankList=tankList,
                           value='')


@app.route('/')
@app.route('/ucloud')
def ucloud():
    bios_config = BiosConfigForm()
    return render_template("ucloud.html",
                           bios_config_form=bios_config,
                           CountEventNow=0,
                           value='')

