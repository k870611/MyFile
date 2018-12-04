#!flask/bin/python
import sys
import os

# sys.path.append(os.path.join(os.environ['UserProfile'], 'Desktop\\Formal\\KyLin'))
dir_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.dirname(dir_path)))
from app import app

app.run(debug=True)

'''
import os

port = int(os.getenv("PORT", 9099))
host = '127.0.0.1'
app.run(host=host, port=port)
'''
