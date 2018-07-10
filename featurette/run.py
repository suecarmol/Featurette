#!venv/bin/python
import os

from app import app

try:
    host = os.environ['HOST']
except:
    host = '0.0.0.0'

try:
    port = int(os.environ['PORT'])
except:
    port = 5000


app.run(debug=True, host=host, port=port)
