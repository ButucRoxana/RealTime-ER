from flask import render_template

from . import main
from .. import login_manager
from realtime_er.models import User, Patient, PatientFile, Hospital, Code, Ambulance, Doctor, Er
from realtime_er import db
from datetime import datetime


@main.route('/')
def index():
    # db.session.add(User(username='ambulance',
    #                     first_name='ambulance',
    #                     last_name='admin',
    #                     email='ambulance@email.com',
    #                     birthday=datetime(1985, 3, 27),
    #                     gender=1,
    #                     type=2,
    #                     phone='0736458921',
    #                     password='er'))
    # db.session.add(Code(color=0,
    #                     waiting_time=10))
    # db.session.add(Code(color=1,
    #                     waiting_time=30))
    # db.session.add(Code(color=2,
    #                     waiting_time=60))
    # db.session.add(Code(color=3,
    #                     waiting_time=90))
    # db.session.add(Code(color=4,
    #                     waiting_time=100))
    # db.session.commit()
    return render_template('index.html')


@main.route('desprenoi')
def despre_noi():
    return render_template('desprenoi.html')


@main.route('medici')
def medici():
    return render_template('medici.html')


@main.route('spitalepartenere')
def spitale_partenere():
    return render_template('spitalepartenere.html')


@main.route('contact')
def contact():
    return render_template('contact.html')


