from datetime import datetime
import json
from requests import get
from app import app, bcrypt, login_manager
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
from models import User, ProductArea, Client, FeatureRequest
from db import session
from config import Auth


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = session.query(User).filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                user.authenticated = True
                session.commit()
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
    return session.query(User).get(user_id)


@app.route('/gCallback')
def callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            session.add(user)
            session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    session.commit()
    logout_user()
    return render_template('login.html')


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    return render_template('index.html')


@app.route('/addFeature', methods=['POST', 'GET'])
@login_required
def addFeature():
    return render_template('addFeature.html')


@app.route('/editFeature')
@login_required
def editFeature():
    return render_template('editFeature.html')


def checkPriorities(client_id, new_client_priority, new_title):
    # initializing priorities dictionary
    priorities_dict = {}
    # find all active feature requests (with date_finished = None)
    features_same_client = FeatureRequest.query.filter(FeatureRequest.client_id == client_id)\
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
        feature_request = FeatureRequest.query.filter(FeatureRequest.title == old_title)\
            .filter(FeatureRequest.client_priority == new_client_priority)\
            .filter(FeatureRequest.client_id == client_id)\
            .one()

        feature_request.client_priority = int(old_key)
        session.add(feature_request)
        session.commit()


@app.route('/finishFeature', methods=['POST'])
@login_required
def finishFeature():
    feature_request_id = request.form['feature_request_id']
    feature_request = FeatureRequest.query.get(feature_request_id)
    feature_request.date_finished = str(datetime.now())
    feature_request.client_priority = 0
    session.commit()
    message = 'The feature request has been marked as Done'
    flash(message)
    return redirect('/')


@app.route('/deleteFeature', methods=['POST'])
@login_required
def deleteFeature():
    feature_request_id = request.form['feature_request_id']
    feature_request = FeatureRequest.query.get(feature_request_id)
    session.delete(feature_request)
    session.commit()
    message = 'The feature request has been deleted'
    flash(message)
    return redirect('/')


@app.route('/users')
@login_required
def users():
    return render_template('users.html')


@app.route('/addUser')
@login_required
def addUsers():
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
        session.commit()
        message = 'The user has been edited successfully'
        flash(message)
        return redirect('/users')


@app.route('/deleteUser', methods=['POST'])
@login_required
def deleteUser():
    user_id = request.form['user_id']
    if int(current_user.id) != int(user_id):
        user = User.query.get(user_id)
        session.delete(user)
        session.commit()
        message = 'The user has been deleted'
        flash(message)
        return redirect('/users')
    else:
        message = 'You cannot delete yourself'
        flash(message)
        return redirect('/users')


@app.route('/clients', methods=['POST', 'GET'])
@login_required
def clients():
    return render_template('clients.html')


@app.route('/addClient')
@login_required
def addClient():
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
        session.commit()
        message = 'The client has been modified successfully'
        flash(message)
        return redirect('/clients')


@app.route('/deleteClient', methods=['POST'])
@login_required
def deleteClient():
    client_id = request.form['client_id']
    client = Client.query.get(client_id)
    session.delete(client)
    session.commit()
    message = 'The client has been deleted'
    flash(message)
    return redirect('/clients')


@app.route('/productAreas', methods=['POST', 'GET'])
@login_required
def productAreas():
    return render_template('productAreas.html')


@app.route('/addProductArea')
@login_required
def addProductArea():
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
        session.commit()
        message = 'The product area has been modified successfully'
        flash(message)
        return redirect('/productAreas')


@app.route('/deleteProductArea', methods=['POST'])
@login_required
def deleteProductArea():
    product_area_id = request.form['product_area_id']
    product_area = ProductArea.query.get(product_area_id)
    session.delete(product_area)
    session.commit()
    message = 'The product area has been deleted'
    flash(message)
    return redirect('/productAreas')


@app.errorhandler(401)
def custom_401(error):
    return render_template('login.html', errors=error)


@app.errorhandler(404)
def custom_404(error):
    return render_template('404.html')
