from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from . import main
from .. import login_manager
from realtime_er.models import User, Patient, PatientFile, Hospital, Code, Ambulance, Doctor, Er
from realtime_er import db
from datetime import datetime
from .forms import ContactForm, AutentificareForm, RecuperareContForm
from .forms import ContactForm, AmbulanceForgotPassForm, AmbulancePacients, AmbulanceRegisterPacient


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
    if form.validate_on_submit():
        if form.salveaza.data:
            # Find user - it's current_user
            user = User.query.filter_by(user_id=current_user.user_id).first()
            if User.check_password(user, form.oldPassword.data):
                print 'OK'
                if form.newPassword.data == form.repeatNewPassword.data:
                    # Set the new password
                    user.password = form.newPassword.data
                    db.session.commit()
                    # Redirect to the login page for the user to login with the new password
                    logout_user()
                    return redirect(url_for('main.autentificare'))
                else:
                    flash("Parola nu coincide cu cea de mai sus!")
            else:
                flash("Parola veche nu coincide cu cea a user-ului!")

    return render_template('ambulanceChangePass.html', form=form)


@main.route('ambulancePatientList', methods=["GET", "POST"])
def ambulance_patient_list():
    form = AmbulancePacients()

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
    print 'here'
    if form.forgot_password.data:
        print 'here2'
        recuperare_cont_form = RecuperareContForm()
        return render_template('recuperare_cont.html', form=recuperare_cont_form)
    print 'here3'
    if form.validate_on_submit():
        print 'here4'
        if form.intra_in_cont.data:
            print 'here5'
            user = User.get_by_username(form.nume.data)
            type = tipuri_cont[form.tip_cont.data]
            print user.check_cont_type(type, form.nume.data)
            if user is not None and user.check_password(form.parola.data) and user.check_cont_type(type, form.nume.data):
                login_user(user, form.remember_me.data)
                #print user
                #print user.doctor
                #print user.ambulance
                #print user.type

                #if user.doctor:
                #    return render_template('user_doctor.html', user=user)
                #elif user.er:
                #    flash("ER")
                #    pass
                #elif user.ambulance:
                #    flash("AMBULANCE")
                #    return render_template('ambulanceHome.html', user=user)
                #    pass
                #elif user.patient:
                #    flash("PATIENT")
                #    pass
                if user.type == 1:
                    return redirect(url_for('main.user_doctor', user=user))
                elif user.type == 3:
                    flash("ER")
                    pass
                elif user.type == 2:
                    flash("AMBULANCE")
                    return redirect(url_for('main.ambulance_home'))
                    pass
                elif user.patient == 0:
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


@main.route("user_doctor")
def user_doctor():
    user = User.get_by_username(current_user.username)
    return render_template("user_doctor.html", user=user)