from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from realtime_er import db


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    birthday = db.Column(db.DateTime())
    gender = db.Column(db.Integer)  # 0 for female - 1 for male
    type = db.Column(db.Integer)  # 0 for patient - 1 for doctor - 2 for ambulance - 3 for er
    phone = db.Column(db.String)
    patient = db.relationship('Patient', backref='userPatient', lazy='dynamic')
    ambulance = db.relationship('Ambulance', backref='userAmbulance', lazy='dynamic')
    doctor = db.relationship('Doctor', backref='userDoctor', lazy='dynamic')
    er = db.relationship('Er', backref='userEr', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_cont_type(self, type, username):
        new_user = User.query.filter_by(username=username).first()
        return new_user.type == type

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    cnp = db.Column(db.Integer, unique=True)
    patient_file = db.relationship('PatientFile', backref='patientPatientFile', lazy='dynamic')


class Hospital(db.Model):
    hospital_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(250))
    doctor = db.relationship('Doctor', backref='doctor', lazy='dynamic')
    er = db.relationship('Er', backref='er', lazy='dynamic')
    patient_file = db.relationship('PatientFile', backref='hospitalPatientFile', lazy='dynamic')


class Doctor(db.Model):
    doctor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.hospital_id'), nullable=False)


class Ambulance(db.Model):
    ambulance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String)
    registration_number = db.Column(db.String(10))


class Er(db.Model):
    er_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.hospital_id'), nullable=False)


class PatientFile(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.hospital_id'), nullable=False)
    code_id = db.Column(db.Integer, db.ForeignKey('code.code_id'), nullable=False)
    observations = db.Column(db.String)
    treatment = db.Column(db.String)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.Integer)  # 0 pending - 1 closed
    attached_unit = db.Column(db.Integer)  # 0 ambulance - 1 er


class Code(db.Model):
    code_id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Integer)  # 0 = red, 1 = yellow, 2 = green, 3 = blue, 4 = white
    waiting_time = db.Column(db.Integer)  # time in minutes
    patient_file = db.relationship('PatientFile', backref='codePatientFile', lazy='dynamic')

