from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Open Susie'}  # fake user
    return render_template('index.html',
                           title='Featurette - Home',
                           user=user)
