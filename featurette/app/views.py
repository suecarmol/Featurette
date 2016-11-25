from app import app
from flask import render_template
from flask_login import login_required


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


# @app.route('/gCallback')
# def callback():
#     # Redirect user to home page if already logged in.
#     if current_user is not None and current_user.is_authenticated:
#         return redirect(url_for('index'))
#     if 'error' in request.args:
#         if request.args.get('error') == 'access_denied':
#             return 'You denied access.'
#         return 'Error encountered.'
#     if 'code' not in request.args and 'state' not in request.args:
#         return redirect(url_for('login'))
#     else:
#         # Execution reaches here when user has
#         # successfully authenticated our app.
#         google = get_google_auth(state=session['oauth_state'])
#         try:
#             token = google.fetch_token(
#                 Auth.TOKEN_URI,
#                 client_secret=Auth.CLIENT_SECRET,
#                 authorization_response=request.url)
#         except HTTPError:
#             return 'HTTPError occurred.'
#         google = get_google_auth(token=token)
#         resp = google.get(Auth.USER_INFO)
#         if resp.status_code == 200:
#             user_data = resp.json()
#             email = user_data['email']
#             user = User.query.filter_by(email=email).first()
#             if user is None:
#                 user = User()
#                 user.email = email
#             user.name = user_data['name']
#             print(token)
#             user.tokens = json.dumps(token)
#             user.avatar = user_data['picture']
#             session.add(user)
#             session.commit()
#             login_user(user)
#             return redirect(url_for('index'))
#         return 'Could not fetch your information.'
#
#
# def get_google_auth(state=None, token=None):
#     if token:
#         return OAuth2Session(Auth.CLIENT_ID, token=token)
#     if state:
#         return OAuth2Session(
#             Auth.CLIENT_ID,
#             state=state,
#             redirect_uri=Auth.REDIRECT_URI)
#     oauth = OAuth2Session(
#         Auth.CLIENT_ID,
#         redirect_uri=Auth.REDIRECT_URI,
#         scope=Auth.SCOPE)
#     return oauth


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
    return render_template('editUser.html')


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
    return render_template('editClient.html')


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
    return render_template('editProductArea.html')


@app.errorhandler(401)
def custom_401(error):
    return render_template('login.html', errors=error)


@app.errorhandler(404)
def custom_404(error):
    return render_template('404.html')
