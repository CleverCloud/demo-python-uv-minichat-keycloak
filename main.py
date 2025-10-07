import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRESQL_ADDON_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(50), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).limit(50).all()
    return jsonify([{
        'pseudo': m.pseudo,
        'contenu': m.contenu,
        'timestamp': m.timestamp.isoformat()
    } for m in reversed(messages)])

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.json
    message = Message(pseudo=data['pseudo'], contenu=data['contenu'])
    db.session.add(message)
    db.session.commit()
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
