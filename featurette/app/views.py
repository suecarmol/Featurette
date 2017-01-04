from app import app
from flask import render_template


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/addFeature', methods=['POST', 'GET'])
def addFeature():
    return render_template('addFeature.html')


@app.route('/editFeature', methods=['POST', 'GET'])
def editFeature():
    return render_template('editFeature.html')


@app.route('/users', methods=['POST', 'GET'])
def users():
    return render_template('users.html')


@app.route('/addUser', methods=['POST', 'GET'])
def addUsers():
    return render_template('addUser.html')


@app.route('/editUser', methods=['POST', 'GET'])
def editUser():
    return render_template('editUser.html')


@app.route('/clients', methods=['POST', 'GET'])
def clients():
    return render_template('clients.html')


@app.route('/addClient', methods=['POST', 'GET'])
def addClient():
    return render_template('addClient.html')


@app.route('/editClient', methods=['POST', 'GET'])
def editClient():
    return render_template('editClient.html')


@app.route('/productAreas', methods=['POST', 'GET'])
def productAreas():
    return render_template('productAreas.html')


@app.route('/addProductArea', methods=['POST', 'GET'])
def addProductArea():
    return render_template('addProductArea.html')


@app.route('/editProductArea', methods=['POST', 'GET'])
def editProductArea():
    return render_template('editProductArea.html')


@app.errorhandler(404)
def custom_404(error):
    return render_template('404.html')
