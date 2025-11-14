
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Admin {self.username}>"

class Department(db.Model):
    __tablename__ = 'department'

    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    doctors_registered = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctors = db.relationship('Doctor', backref='department', lazy=True)
    appointments = db.relationship('Appointment', backref='department_info', lazy=True)

    def __repr__(self):
        return f"<Department {self.department_name}>"

class Doctor(db.Model):
    __tablename__ = 'doctor'

    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    specialization_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    availability = db.Column(db.Text)  # could be JSON string
    status = db.Column(db.String(50), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    availability_slots = db.relationship('Availability', backref='doctor_info', lazy=True)

    def __repr__(self):
        return f"<Doctor {self.name} - {self.status}>"

class Patient(db.Model):
    __tablename__ = 'patient'

    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(15))
    address = db.Column(db.String(255))
    status = db.Column(db.String(50), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def __repr__(self):
        return f"<Patient {self.name}>"

class Appointment(db.Model):
    __tablename__ = 'appointment'

    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(20), nullable=False)
    mode = db.Column(db.String(20), default="In-person")
    status = db.Column(db.String(30), default="Booked")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    treatment = db.relationship('Treatment', backref='appointment', uselist=False)

    def __repr__(self):
        return f"<Appointment Doctor:{self.doctor_id}, Patient:{self.patient_id}, Date:{self.date}>"

class Treatment(db.Model):
    __tablename__ = 'treatment'

    treatment_id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.appointment_id'), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Treatment for Appointment {self.appointment_id}>"

class Availability(db.Model):
    __tablename__ = 'availability'

    availability_id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(50))
    status = db.Column(db.String(30), default="Available")

    def __repr__(self):
        return f"<Availability Doctor:{self.doctor_id} {self.date} - {self.status}>"

def init_admin():
    """Create a default admin if not exists."""
    from werkzeug.security import generate_password_hash
    existing_admin = Admin.query.first()
    if not existing_admin:
        admin = Admin(username='admin', password=generate_password_hash('admin123'), email='admin@hospital.com')
        db.session.add(admin)
        db.session.commit()
        print("Default admin created: username=admin, password=admin123")
    else:
        print("Admin already exists.")
