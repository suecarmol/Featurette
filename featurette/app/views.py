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
    #TODO: add ticket URL
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
        date_finished = None
        feature_request = FeatureRequest(title, description, client_id, client_priority, target_date, product_area_id, user_id, date_finished)
        db.session.add(feature_request)
        db.session.commit()
        return redirect('/')
    else:
        clients = Client.query.all()
        product_areas = ProductArea.query.all()
        return render_template('addFeature.html', clients=clients, product_areas=product_areas)

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
