from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/addFeature')
def addFeature():
    return render_template('addFeature.html')

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/addUser')
@app.route('/addUsers')
def addUsers():
    return render_template('addUser.html')

@app.route('/clients')
def clients():
    return render_template('clients.html')

@app.route('/addClients')
@app.route('/addClient')
def AddClient():
    return render_template('addClient.html')

@app.route('/productAreas')
def productAreas():
    return render_template('productAreas.html')

@app.route('/addProductAreas')
@app.route('/addProductArea')
def addProductArea():
    return render_template('addProductArea.html')
