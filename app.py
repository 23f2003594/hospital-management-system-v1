# app.py
from flask import Flask
from models import db, init_admin

app = Flask(__name__)

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()       # Creates all tables
    init_admin()          # Adds default admin if not present

print("Database setup completed successfully!")

if __name__ == '__main__':
    app.run(debug=True)
