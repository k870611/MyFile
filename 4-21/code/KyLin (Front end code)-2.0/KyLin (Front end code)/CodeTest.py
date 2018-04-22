# -*- coding: utf-8 -*-
from datetime import datetime
import datetime as date
import base64
import re

print(datetime.now())
print(datetime.strptime('2018-03-31 00:00', '%Y-%m-%d %H:%M'))
a = [i for i in range(5)]

print(a)
print(len(a)/2)

abc = "abc"
z = abc.replace('a', '1')
print(abc.__contains__('b'))
print(z)

a = str(base64.b64encode('123456'.encode('utf-8')), 'utf-8')
print(a)

b = str(base64.b64decode(a.encode('utf-8')), 'utf-8')
print(b)

if b is 'kkkk1234':
    print('equal')

situation = {
    '0': 'Power Off',
    '1': 'Power On',
    '2': 'Warning'
}.get('', "x")

print(situation)
print('25℃')

st = '          12345689          0          '
print(st.find(','))

print(st.strip())

print(re.sub('\s', '', st))

deadline = datetime.now() + date.timedelta(minutes=-30)
print(deadline)



'''
import socket, uuid
my_computer_name = socket.getfqdn(socket.gethostname())
ip = socket.gethostbyname(my_computer_name)

mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
mac = (": ".join([mac[e:e+2] for e in range(0, 11, 2)])).upper()

main_server_info = []
for i in range(10):
    main_server_info.append({'slot': (i+1), 'ip': ip, 'mac': mac, 'situation': (i % 3)})
'''

'''
import logging, os
from logging.handlers import RotatingFileHandler
if not os.path.exists('logs'):
    os.mkdir('logs')

LOG_FILENAME = 'logs/access.log'

formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=5)
handler.setLevel(logging.ERROR)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
'''



