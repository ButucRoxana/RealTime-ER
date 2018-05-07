from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user

from . import main
from .. import login_manager
from realtime_er.models import User, Patient, PatientFile, Hospital, Code, Ambulance, Doctor, Er
from realtime_er import db
from datetime import datetime
from .forms import ContactForm, AutentificareForm, RecuperareContForm
from .forms import ContactForm, AmbulanceForgotPassForm, AmbulanceTransferPacients, AmbulanceRegisterPacient


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


@main.route('medici/specializare')
def specializare():
    return render_template('specializare.html')


@main.route('spitalepartenere')
def spitale_partenere():
    return render_template('spitalepartenere.html')


@main.route('contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('ambulanceHome', methods=["GET", "POST"])
def ambulance_home():
    return render_template('ambulanceHome.html')


@main.route('ambulanceChangePass', methods=["GET", "POST"])
def ambulance_change_pass():
    form = AmbulanceForgotPassForm()
    return render_template('ambulanceChangePass.html', form=form)


@main.route('ambulancePatientList', methods=["GET", "POST"])
def ambulance_patient_list():
    form = AmbulanceTransferPacients()
    return render_template('ambulancePatientList.html', form=form)


@main.route('ambulanceRegisterPatient', methods=["GET", "POST"])
def ambulance_register_patient():
    form = AmbulanceRegisterPacient()
    # this has to be replaced with the right page
    return render_template('ambulanceHome.html', form=form)

tipuri_cont = {
    "Medic": 1,
    "Ambulanta": 2,
    "Pacient": 0,
    "ER": 3
}


@main.route('autentificare', methods=["GET", "POST"])
def autentificare():
    form = AutentificareForm()
    if form.forgot_password.data:
        recuperare_cont_form = RecuperareContForm()
        return render_template('recuperare_cont.html', form=recuperare_cont_form)
    if form.validate_on_submit():
        if form.intra_in_cont.data:
            user = User.get_by_username(form.nume.data)
            type = tipuri_cont[form.tip_cont.data]
            if user is not None and user.check_password(form.parola.data) and user.check_cont_type(type, form.nume.data):
                login_user(user, form.remember_me.data)
                if user.doctor:
                    return render_template('user_doctor.html', user=user)
                elif user.er:
                    flash("ER")
                    pass
                elif user.ambulance:
                    flash("AMBULANCE")
                    pass
                elif user.patient:
                    flash("PATIENT")
                    pass
                flash("Autentifcare reusita pentru utilizatorul: {}.".format(user.username))
            else:
                flash("Date incorecte")
        # elif form.forgot_password.data:
        #     recuperare_cont_form = RecuperareContForm()
        #     return render_template('recuperare_cont.html', form=recuperare_cont_form)
    return render_template('autentificare.html', form=form)


@main.route("deconectare")
def deconectare():
    logout_user()
    return render_template("index.html")