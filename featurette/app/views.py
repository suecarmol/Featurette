from app import app
from flask import render_template
from models import User, ProductArea, Client, FeatureRequest

@app.route('/')
@app.route('/index')
def index():
    feature_requests = FeatureRequest.query.all()
    return render_template('index.html', feature_requests=feature_requests)

@app.route('/addFeature')
def addFeature():
    return render_template('addFeature.html')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/addUser')
@app.route('/addUsers')
def addUsers():
    return render_template('addUser.html')

@app.route('/clients')
def clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/addClients')
@app.route('/addClient')
def AddClient():
    return render_template('addClient.html')

@app.route('/productAreas')
def productAreas():
    product_areas = ProductArea.query.all()
    return render_template('productAreas.html', product_areas=product_areas)

@app.route('/addProductAreas')
@app.route('/addProductArea')
def addProductArea():
    return render_template('addProductArea.html')
