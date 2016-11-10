from datetime import datetime

from app import app, bcrypt, login_manager
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
from models import User, ProductArea, Client, FeatureRequest, db


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                user.authenticated = True
                db.session.commit()
                login_user(user, remember=True)
                return redirect('/')
            else:
                errors = 'Email or password are incorrect'
                return render_template('login.html', errors=errors)
        else:
            errors = 'User does not exist'
            return render_template('login.html', errors=errors)
    else:
        return render_template('login.html')


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.commit()
    logout_user()
    return render_template('login.html')


@app.route('/')
@login_required
def index():
    feature_requests = FeatureRequest.query.all()
    return render_template('index.html', feature_requests=feature_requests)


@app.route('/addFeature', methods=['GET', 'POST'])
@login_required
def addFeature():
    if request.method == 'POST':

        title = request.form['request_title']
        description = request.form['request_description']
        client_id = request.form['client']
        client_priority = request.form['client_priority']
        target_date = request.form['target_date']
        product_area_id = request.form['product_area']
        user = current_user
        user_id = current_user.id
        ticket_url = request.form['ticket_url']
        date_finished = None

        checkPriorities(client_id, client_priority, title)
        feature_request = FeatureRequest(title, description, client_id, client_priority,
            product_area_id, user_id, target_date, ticket_url, date_finished)

        db.session.add(feature_request)
        db.session.commit()
        message = 'The feature request has been added successfully'
        flash(message)
        return redirect('/')
    else:
        clients = Client.query.all()
        product_areas = ProductArea.query.all()
        return render_template('addFeature.html', clients=clients,
                               product_areas=product_areas)


@app.route('/editFeature', methods=['POST', 'GET'])
@login_required
def editFeature():
    if request.method == 'GET':
        feature_request_id = request.args['edit_feature_request']
        feature_request = FeatureRequest.query.get(feature_request_id)
        clients = Client.query.all()
        product_areas = ProductArea.query.all()
        return render_template('editFeature.html', feature_request=feature_request,
                               clients=clients, product_areas=product_areas)
    else:
        feature_request_id = request.form['feature_request_id']
        feature_request = FeatureRequest.query.get(feature_request_id)
        title = request.form['request_title']
        description = request.form['request_description']
        client_id = request.form['client']
        new_client_priority = request.form['client_priority']
        target_date = request.form['target_date']
        product_area_id = request.form['product_area']
        ticket_url = request.form['ticket_url']
        user = current_user

        checkPriorities(client_id, new_client_priority, title)

        feature_request.title = title
        feature_request.description = description
        feature_request.client_id = client_id
        feature_request.client_priority = new_client_priority
        feature_request.target_date = target_date
        feature_request.product_area_id = product_area_id
        feature_request.ticket_url = ticket_url
        feature_request.user_id = user.id
        db.session.commit()
        message = 'The feature request has been edited successfully'
        flash(message)
        return redirect('/')


def checkPriorities(client_id, new_client_priority, new_title):
    # initializing priorities dictionary
    priorities_dict = {}
    # find all active feature requests (with date_finished = None)
    features_same_client = FeatureRequest.query.filter(FeatureRequest.client_id==client_id)\
        .filter(FeatureRequest.date_finished == None)
    # filling dictionary
    for feature_same_client in features_same_client:
        priorities_dict[str(feature_same_client.client_priority)] = feature_same_client.title
    # checking if priority number exists
    if str(new_client_priority) in priorities_dict:
        # get data of existing priority (removing the key)
        old_key = new_client_priority
        old_title = priorities_dict[str(old_key)]
        # while key exists continue incrementing by 1
        while str(old_key) in priorities_dict:
            aux = int(old_key)
            aux = aux + 1
            old_key = str(aux)
        del priorities_dict[str(new_client_priority)]
        # add new priority and title
        priorities_dict[str(new_client_priority)] = new_title
        # add old priority and title
        priorities_dict[str(old_key)] = old_title
        # get old Feature Request that matches the parameters
        feature_request = FeatureRequest.query.filter(FeatureRequest.title==old_title)\
            .filter(FeatureRequest.client_priority==new_client_priority)\
            .filter(FeatureRequest.client_id==client_id)\
            .one()

        feature_request.client_priority = int(old_key)
        db.session.add(feature_request)
        db.session.commit()


@app.route('/finishFeature', methods=['POST'])
@login_required
def finishFeature():
    feature_request_id = request.form['feature_request_id']
    feature_request = FeatureRequest.query.get(feature_request_id)
    feature_request.date_finished = str(datetime.now())
    feature_request.client_priority = 0
    db.session.commit()
    message = 'The feature request has been marked as Done'
    flash(message)
    return redirect('/')


@app.route('/deleteFeature', methods=['POST'])
@login_required
def deleteFeature():
    feature_request_id = request.form['feature_request_id']
    feature_request = FeatureRequest.query.get(feature_request_id)
    db.session.delete(feature_request)
    db.session.commit()
    message = 'The feature request has been deleted'
    flash(message)
    return redirect('/')


@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/addUser', methods=['GET', 'POST'])
@login_required
def addUsers():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username, email, bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        message = 'The user has been added successfully'
        flash(message)
        return redirect('/users')
    else:
        return render_template('addUser.html')


@app.route('/editUser', methods=['POST', 'GET'])
@login_required
def editUser():
    if request.method == 'GET':
        user_id = request.args['user_id']
        user = User.query.get(user_id)
        return render_template('editUser.html', user=user)
    else:
        user_id = request.form['user_id']
        user = User.query.get(user_id)
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user.username = username
        user.email = email
        user.password = bcrypt.generate_password_hash(password)
        db.session.commit()
        message = 'The user has been edited successfully'
        flash(message)
        return redirect('/users')


@app.route('/deleteUser', methods=['POST'])
@login_required
def deleteUser():
    user_id = request.form['user_id']
    if int(current_user.id) != int(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        message = 'The user has been deleted'
        flash(message)
        return redirect('/users')
    else:
        message = 'You cannot delete yourself'
        flash(message)
        return redirect('/users')

@app.route('/clients')
@login_required
def clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/addClient', methods=['GET', 'POST'])
@login_required
def addClient():
    if request.method == 'POST':
        client_name = request.form['client_name']
        client = Client(client_name)
        db.session.add(client)
        db.session.commit()
        message = 'The client has been added successfully'
        flash(message)
        return redirect('/clients')
    else:
        return render_template('addClient.html')


@app.route('/editClient', methods=['POST', 'GET'])
@login_required
def editClient():
    if request.method == 'GET':
        client_id = request.args['client_id']
        client = Client.query.get(client_id)
        return render_template('editClient.html', client=client)
    else:
        client_id = request.form['client_id']
        client = Client.query.get(client_id)
        client_name = request.form['client_name']
        client.name = client_name
        db.session.commit()
        message = 'The client has been modified successfully'
        flash(message)
        return redirect('/clients')


@app.route('/deleteClient', methods=['POST'])
@login_required
def deleteClient():
    client_id = request.form['client_id']
    client = Client.query.get(client_id)
    db.session.delete(client)
    db.session.commit()
    message = 'The client has been deleted'
    flash(message)
    return redirect('/clients')


@app.route('/productAreas')
@login_required
def productAreas():
    product_areas = ProductArea.query.all()
    return render_template('productAreas.html', product_areas=product_areas)


@app.route('/addProductArea', methods=['GET', 'POST'])
@login_required
def addProductArea():
    if request.method == 'POST':
        product_area_name = request.form['product_area_name']
        product_area = ProductArea(product_area_name)
        db.session.add(product_area)
        db.session.commit()
        message = 'The product area has been added successfully'
        flash(message)
        return redirect('/productAreas')
    else:
        return render_template('addProductArea.html')


@app.route('/editProductArea', methods=['POST', 'GET'])
@login_required
def editProductArea():
    if request.method == 'GET':
        product_area_id = request.args['product_area_id']
        product_area = ProductArea.query.get(product_area_id)
        return render_template('editProductArea.html', product_area=product_area)
    else:
        product_area_id = request.form['product_area_id']
        product_area = ProductArea.query.get(product_area_id)
        product_area_name = request.form['product_area_name']
        product_area.name = product_area_name
        db.session.commit()
        message = 'The product area has been modified successfully'
        flash(message)
        return redirect('/productAreas')


@app.route('/deleteProductArea', methods=['POST'])
@login_required
def deleteProductArea():
    product_area_id = request.form['product_area_id']
    product_area = ProductArea.query.get(product_area_id)
    db.session.delete(product_area)
    db.session.commit()
    message = 'The product area has been deleted'
    flash(message)
    return redirect('/productAreas')


@app.errorhandler(401)
def custom_401(error):
    return render_template('login.html', errors=error)


@app.errorhandler(404)
def custom_404(error):
    return render_template('404.html')
