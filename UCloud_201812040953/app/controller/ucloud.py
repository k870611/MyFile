import os
import platform
import subprocess
from datetime import datetime

from flask import render_template, flash, request, jsonify
import sqlalchemy

from app import app, db
from app.models import Tank, Server, ServerDetail, ServerSdr, ServerLan, ServerFru
from app.forms import BiosConfigForm


def arp_check(ip):
    if platform.system() == "Windows":
        os.system("arp -a {} > temp.txt".format(ip))
    else:
        os.system('arp -e {} > temp.txt'.format(ip))

    ip_can_find = False

    with open('temp.txt') as fp:
        for line in fp:
            if platform.system() == "Windows":
                info = line.split()[:2]

            else:
                info = line.split()[:3:2]

            print(info)
            if info[0] == ip:
                ip_can_find = True

    os.remove('temp.txt')
    return ip_can_find


@app.route('/bios_config_form_action', methods=['GET', 'POST'])
def bios_config_form_action():
    print("into bios_config_form_action3")

    bios_form = request.get_json(force=True).get('bios_form')

    if len(bios_form) > 1 and bios_form is not None:
        bios_form = bios_form[1:]

    print(bios_form)

    return jsonify({'Success': 'True'})


