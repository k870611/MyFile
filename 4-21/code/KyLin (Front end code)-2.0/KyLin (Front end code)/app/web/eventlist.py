from flask import render_template
from flask_login import login_required

from app import app
from app.models import EventWarning, EventDevice, EventSystem, EventNow


@app.route('/eventWarning', methods=['GET', 'POST'])
@login_required
def eventWarning():

    dtEventWarning = EventWarning.query.all()
    EventList = []

    for e in dtEventWarning:
        EventList.append({
            'table': 'event_warning',
            'level': e.event_warning_level,
            'name': e.event_warning_name,
            'description': e.event_warning_description,
            'time': e.event_warning_time,
            'action': e.event_warning_action,
        })
    EventCount = CountEventNow()

    return render_template("eventlist.html", EventList=EventList, ShowInfo='warning', CountEventNow=EventCount)


@app.route('/eventDevice', methods=['GET', 'POST'])
@login_required
def eventDevice():

    dtEventDevice = EventDevice.query.all()
    EventList = []
    for e in dtEventDevice:
        EventList.append({
            'table': 'event_device',
            'level': e.event_device_level,
            'name': e.event_device_name,
            'description': e.event_device_description,
            'time': e.event_device_time,
            'action': e.event_device_action,
        })

    EventCount = CountEventNow()
    return render_template("eventlist.html", EventList=EventList, ShowInfo='device', CountEventNow=EventCount)


@app.route('/eventSystem', methods=['GET', 'POST'])
@login_required
def eventSystem():

    dtEventSystem = EventSystem.query.all()
    EventList = []
    for e in dtEventSystem:
        EventList.append({
            'table': 'event_system',
            'level': e.event_system_level,
            'name': e.event_system_name,
            'description': e.event_system_description,
            'time': e.event_system_time,
            'action': e.event_system_action,
        })

    EventCount = CountEventNow()
    return render_template("eventlist.html", EventList=EventList, ShowInfo='system', CountEventNow=EventCount)


@app.route('/eventNow', methods=['GET', 'POST'])
@login_required
def eventNow():

    dtEventNow = EventNow.query.all()
    EventList = []
    for e in dtEventNow:
        EventList.append({
            'table': 'event_now',
            'level': e.event_now_level,
            'name': e.event_now_name,
            'description': e.event_now_description,
            'time': e.event_now_time,
            'action': e.event_now_action,
        })

    EventCount = CountEventNow()
    return render_template("eventlist.html", EventList=EventList, ShowInfo='now', CountEventNow=EventCount)


def CountEventNow():
    Count = len(EventNow.query.all())
    return Count
