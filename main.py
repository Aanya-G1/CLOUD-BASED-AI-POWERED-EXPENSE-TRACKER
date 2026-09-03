from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import joblib
import urllib.parse


app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = "supersecurekey123"
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:D96Sl7hKSHATrkSJ@db.jezpksiujzvsifiwtlrp.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImplenBrc2l1anp2c2lmaXd0bHJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMyMjczNTQsImV4cCI6MjA3ODU4NzM1NH0.bXX6YcS2fb0DNxI-tO_t9dyZ7qXO1UkDcBKhg2QWzws"
db = SQLAlchemy(app)

# Load ML model and vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Import routes after app/db/model setup
from routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
