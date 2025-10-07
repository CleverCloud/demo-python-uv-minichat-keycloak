import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRESQL_ADDON_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

db = SQLAlchemy(app)
oauth = OAuth(app)

keycloak = oauth.register(
    name='keycloak',
    client_id=os.environ.get('KEYCLOAK_CLIENT_ID'),
    client_secret=os.environ.get('KEYCLOAK_CLIENT_SECRET'),
    server_metadata_url=f"{os.environ.get('CC_KEYCLOAK_URL')}/realms/{os.environ.get('KEYCLOAK_REALM')}/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid email profile'}
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Non authentifié'}), 401
        return f(*args, **kwargs)
    return decorated_function

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(50), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('secure_index.html')


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return keycloak.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = keycloak.authorize_access_token()
    user_info = token.get('userinfo')
    session['user'] = {
        'username': user_info.get('preferred_username'),
        'email': user_info.get('email'),
        'name': user_info.get('name')
    }
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/user')
def get_user():
    if 'user' in session:
        return jsonify(session['user'])
    return jsonify(None)

@app.route('/messages', methods=['GET'])
@login_required
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).limit(50).all()
    return jsonify([{
        'pseudo': m.pseudo,
        'contenu': m.contenu,
        'timestamp': m.timestamp.isoformat()
    } for m in reversed(messages)])

@app.route('/messages', methods=['POST'])
@login_required
def post_message():
    data = request.json
    user = session['user']
    message = Message(pseudo=user['username'], contenu=data['contenu'])
    db.session.add(message)
    db.session.commit()
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
