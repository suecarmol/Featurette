#!venv/bin/python
import os

from app import app

try:
    host = os.environ['HOST']
except:
    host = '127.0.0.1'

app.run(debug=True, threaded=True, host=host)
