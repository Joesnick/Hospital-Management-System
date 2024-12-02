from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

doctor_patient = db.Table('doctor_patient',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'), primary_key=True)
)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identification_number = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    id_number = db.Column(db.String(20), nullable=False, unique=True)
    license = db.Column(db.String(20), nullable=False, unique=True)
    specialty = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)



class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)  # Nuevo campo
    purpose = db.Column(db.String(200), nullable=False)  # Nuevo campo
    status = db.Column(db.String(20), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)

class Internment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_date = db.Column(db.Date, nullable=False)
    discharge_date = db.Column(db.Date)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    patient = db.relationship('Patient', backref=db.backref('treatments', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('treatments', lazy=True))


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    medicine = db.Column(db.String(100), nullable=False)
    dose = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    patient = db.relationship('Patient', backref='prescriptions')
    doctor = db.relationship('Doctor', backref='prescriptions')
