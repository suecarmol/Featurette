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

@app.route('/users/add')
@app.route('/user/add')
def addUsers():
    return render_template('addUser.html')

@app.route('/clients')
def clients():
    return render_template('clients.html')

@app.route('/clients/add')
@app.route('/client/add')
def AddClient():
    return render_template('addClient.html')

@app.route('/productAreas')
def productAreas():
    return render_template('productAreas.html')

@app.route('/productAreas/add')
@app.route('/productArea/add')
def addProductArea():
    return render_template('addProductArea.html')
