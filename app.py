
from flask import Flask
from models import db, init_admin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()       
    init_admin()          

print("Database setup completed successfully!")

if __name__ == '__main__':
    app.run(debug=True)
