from app import app, bcrypt
from flask import render_template, request, redirect
from models import User, ProductArea, Client, FeatureRequest, db

@app.route('/')
@app.route('/index')
def index():
    feature_requests = FeatureRequest.query.all()
    return render_template('index.html', feature_requests=feature_requests)

@app.route('/addFeature', methods=['GET','POST'])
def addFeature():
    #TODO: insert id of user that is logged in
    #TODO: add algorithm to change priorities per client if priority exists
    if request.method == 'POST':
        title = request.form['request_title']
        description = request.form['request_description']
        client_id = request.form['client']
        client_priority = request.form['client_priority']
        target_date = request.form['target_date']
        product_area_id = request.form['product_area']
        user_id = u'2'
        ticket_url = request.form['ticket_url']
        date_finished = None
        feature_request = FeatureRequest(title, description, client_id, client_priority,
            product_area_id, user_id, target_date, ticket_url, date_finished)
        db.session.add(feature_request)
        db.session.commit()
        return redirect('/')
    else:
        clients = Client.query.all()
        product_areas = ProductArea.query.all()
        return render_template('addFeature.html', clients=clients, product_areas=product_areas)

@app.route('/deleteFeature', methods=['POST'])
@app.route('/deleteFeatures', methods=['POST'])
def deleteFeature():
    feature_request_id = request.form['feature_request_id']
    feature_request = FeatureRequest.query.get(feature_request_id)
    db.session.delete(feature_request)
    db.session.commit()
    return redirect('/')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/addUser', methods=['GET', 'POST'])
@app.route('/addUsers', methods=['GET', 'POST'])
def addUsers():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username, email, bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    else:
        return render_template('addUser.html')

@app.route('/deleteUser', methods=['POST'])
@app.route('/deleteUsers', methods=['POST'])
def deleteUser():
    user_id = request.form['user_id']
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/clients')
def clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/addClients', methods=['GET', 'POST'])
@app.route('/addClient', methods=['GET', 'POST'])
def addClient():
    if request.method == 'POST':
        client_name = request.form['client_name']
        client = Client(client_name)
        db.session.add(client)
        db.session.commit()
        return redirect('/clients')
    else:
        return render_template('addClient.html')

@app.route('/deleteClient', methods=['POST'])
@app.route('/deleteClients', methods=['POST'])
def deleteClient():
    client_id = request.form['client_id']
    client = Client.query.get(client_id)
    db.session.delete(client)
    db.session.commit()
    return redirect('/clients')

@app.route('/productAreas')
def productAreas():
    product_areas = ProductArea.query.all()
    return render_template('productAreas.html', product_areas=product_areas)

@app.route('/addProductAreas', methods=['GET', 'POST'])
@app.route('/addProductArea', methods=['GET', 'POST'])
def addProductArea():
    if request.method == 'POST':
        product_area_name = request.form['product_area_name']
        product_area = ProductArea(product_area_name)
        db.session.add(product_area)
        db.session.commit()
        return redirect('/productAreas')
    else:
        return render_template('addProductArea.html')

@app.route('/editProductArea', methods=['POST', 'GET'])
@app.route('/editProductAreas', methods=['POST', 'GET'])
def editProductArea():
    product_area_id = request.args['product_area_id']
    product_area = ProductArea.query.get(product_area_id)
    if request.method == 'GET':
        return render_template('editProductArea.html', product_area=product_area)
    else:
        product_area_name = request.form['product_area_name']
        product_area.name = product_area_name
        db.session.commit()
        return redirect('/productArea')

@app.route('/deleteProductArea', methods=['POST'])
@app.route('/deleteProductAreas', methods=['POST'])
def deleteProductArea():
    product_area_id = request.form['product_area_id']
    product_area = ProductArea.query.get(product_area_id)
    db.session.delete(product_area)
    db.session.commit()
    return redirect('/productAreas')
