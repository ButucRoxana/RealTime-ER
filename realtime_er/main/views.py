from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from . import main
from .. import login_manager
from realtime_er.models import User, Patient, PatientFile, Hospital, Code, Ambulance, Doctor, Er
from realtime_er import db
from datetime import datetime
from .forms import AutentificareForm, RecuperareContForm
from .forms import ContactForm, AmbulanceForgotPassForm, AmbulancePacients, AmbulanceRegisterPacient, SchimbaParola, \
    PatientFileForm, InregistrareDoctorER, CerereUPU, MobileInregistrareForm, DatePersonaleForm


class Pats(object):
    def __init__(self, name="Unknown name", file_id=0, patient_id=0, color=0):
        self.name = name
        self.file_id = file_id
        self.patient_id = patient_id
        self.color = color

class Spital(object):
    def __init__(self, nume=" ", timp=0, spital_id=0):
        self.nume = nume
        self.timp = timp
        self.spital_id = spital_id

class PatFile(object):
    def __init__(self, nume, datanasterii, cnp, adresa, telefon, email, sex, cod_urgenta, observatii, tratament):
        self.nume = nume
        self.datanasterii = datanasterii
        self.cnp = cnp
        self.adresa = adresa
        self.telefon = telefon
        self.email = email
        self.sex = sex
        self.cod_urgenta = cod_urgenta
        self.observatii = observatii
        self.tratament = tratament


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


@main.route('inregistrarepacient', methods=["GET", "POST"])
def inregistrare_pacient():
    form = PatientFileForm()
    if form.validate_on_submit():
        existingPatient = Patient.query.filter_by(cnp=form.cnp.data).first()
        if existingPatient is None:
            user = User(username=form.cnp.data,
                        first_name=form.nume.data,
                        last_name='',
                        email=form.email.data,
                        birthday= datetime(1985, 3, 27),
                        gender=form.sex.data,
                        type=0,
                        phone=form.telefon.data,
                        password='test')
            db.session.add(user)
            db.session.commit()
            userid = User.query.filter_by(username=form.cnp.data).first().user_id
            patient = Patient(user_id=userid,
                              cnp=form.cnp.data)
            db.session.add(patient)
            db.session.commit()
            codeid = Code.query.filter_by(color=form.cod_urgenta.data).first().code_id
            patientid = Patient.query.filter_by(cnp=form.cnp.data).first().patient_id
            patientFile = PatientFile(patient_id=patientid,
                                      code_id=codeid,
                                      hospital_id=1,
                                      attached_unit=1,
                                      status=0,
                                      treatment=form.tratament.data,
                                      observations=form.observatii.data
                                      )
            db.session.add(patientFile)
            db.session.commit()
        else:
            flash("Pacientul este deja inregisrat!")
        return redirect(url_for('main.erHome'))
    else:
        flash("Date invalide!")
    return render_template('inregistrarePacient.html', form=form)

@main.route('ambulanceRegisterPacient', methods=["GET", "POST"])
def ambulance_register_pacient():
    form = PatientFileForm()
    print form.validate_on_submit()
    if form.validate_on_submit():
        existingPatient = Patient.query.filter_by(cnp=form.cnp.data).first()
        if existingPatient is None:
            user = User(username=form.cnp.data,
                        first_name=form.nume.data,
                        last_name='',
                        email=form.email.data,
                        birthday= datetime(1985, 3, 27),
                        gender=form.sex.data,
                        type=0,
                        phone=form.telefon.data,
                        password='test')
            db.session.add(user)
            db.session.commit()
            userid = User.query.filter_by(username=form.cnp.data).first().user_id
            patient = Patient(user_id=userid,
                              cnp=form.cnp.data)
            db.session.add(patient)
            db.session.commit()
            codeid = Code.query.filter_by(color=form.cod_urgenta.data).first().code_id
            patientid = Patient.query.filter_by(cnp=form.cnp.data).first().patient_id
            patientFile = PatientFile(patient_id=patientid,
                                      code_id=codeid,
                                      hospital_id=1,
                                      attached_unit=0,
                                      status=0,
                                      treatment=form.tratament.data,
                                      observations=form.observatii.data
                                      )
            db.session.add(patientFile)
            db.session.commit()
        else:
            flash("Pacientul este deja inregisrat!")
        return redirect(url_for('main.ambulance_patient_list'))
    else:
        flash("Date invalide!")
    return render_template('ambulanceRegisterPacient.html', form=form)


@main.route('ambulanceTransferPacients', methods=["GET", "POST"])
def ambulance_transfer_patients():
    patient_files = PatientFile.query.filter_by(status=0,
                                                attached_unit=0
                                                )
    for x in patient_files:
        x.attached_unit = 1

    db.session.commit()
    return redirect(url_for('main.ambulance_patient_list'))


@main.route('er', methods=["GET", "POST"])
def erHome():
    patients = []
    patient_files = PatientFile.query.filter_by(status=0,
                                                attached_unit=1
                                                )
    for x in patient_files:
        color = Code.query.filter_by(code_id=x.code_id).first().color
        userid = Patient.query.filter_by(patient_id=x.patient_id).first().user_id
        user = User.query.filter_by(user_id=userid).first()
        name = user.last_name + ' ' + user.first_name
        patient = Pats(name, x.file_id, x.patient_id, color)
        patients.append(patient)
    for y in patients:
        print y.name + "-------------------"
    return render_template('erHome.html', user=current_user, patients=patients)


@main.route('detaliipacient/<int:file_id>', methods=["GET", "POST"])
def detaliipacient(file_id):
    patient_file = PatientFile.query.filter_by(file_id=file_id).first()
    patient = Patient.query.filter_by(patient_id=patient_file.patient_id).first()
    color = Code.query.filter_by(code_id=patient_file.code_id).first().color
    user = User.query.filter_by(user_id=patient.user_id).first()
    p = PatFile(user.last_name + ' ' + user.first_name, user.birthday, patient.cnp, "Str. Fizicienilor", user.phone, user.email, user.gender, color, patient_file.observations, patient_file.treatment)
    form = PatientFileForm(obj=p)
    if form.validate_on_submit():
        patient_file.observations = form.observatii.data
        patient_file.treatment = form.tratament.data
        codeid = Code.query.filter_by(color=form.cod_urgenta.data).first().code_id
        patient_file.code_id = codeid
        db.session.commit()
        return redirect(url_for('main.erHome'))
    return render_template('detaliipacient.html', form=form)

@main.route('detaliipacientDoctor/<int:file_id>', methods=["GET", "POST"])
def detaliipacientDoctor(file_id):
    patient_file = PatientFile.query.filter_by(file_id=file_id).first()
    patient = Patient.query.filter_by(patient_id=patient_file.patient_id).first()
    color = Code.query.filter_by(code_id=patient_file.code_id).first().color
    user = User.query.filter_by(user_id=patient.user_id).first()
    p = PatFile(user.last_name + ' ' + user.first_name, user.birthday, patient.cnp, "Str. Fizicienilor", user.phone, user.email, user.gender, color, patient_file.observations, patient_file.treatment)
    form = PatientFileForm(obj=p)
    if form.validate_on_submit():
        patient_file.observations = form.observatii.data
        patient_file.treatment = form.tratament.data
        codeid = Code.query.filter_by(color=form.cod_urgenta.data).first().code_id
        patient_file.code_id = codeid
        db.session.commit()
        return redirect(url_for('main.user_doctor'))
    return render_template('consulta.html', form=form)


@main.route('ambulanceDetaliipacient/<int:file_id>', methods=["GET", "POST"])
def ambulance_detaliipacient(file_id):
    patient_file = PatientFile.query.filter_by(file_id=file_id).first()
    patient = Patient.query.filter_by(patient_id=patient_file.patient_id).first()
    color = Code.query.filter_by(code_id=patient_file.code_id).first().color
    user = User.query.filter_by(user_id=patient.user_id).first()
    p = PatFile(user.last_name + ' ' + user.first_name, user.birthday, patient.cnp, "Str. Fizicienilor", user.phone, user.email, user.gender, color, patient_file.observations, patient_file.treatment)
    form = PatientFileForm(obj=p)
    if form.validate_on_submit():
        patient_file.observations = form.observatii.data
        patient_file.treatment = form.tratament.data
        codeid = Code.query.filter_by(color=form.cod_urgenta.data).first().code_id
        patient_file.code_id = codeid
        db.session.commit()
        return redirect(url_for('main.ambulance_patient_list'))
    return render_template('ambulanceDetailPacient.html', form=form)



@main.route('consulta/<int:file_id>', methods=["GET", "POST"])
def consulta(file_id):
    patient_file = PatientFile.query.filter_by(file_id=file_id).first()
    patient_file.start_time = datetime.now()
    db.session.commit()
    patient = Patient.query.filter_by(patient_id=patient_file.patient_id).first()
    color = Code.query.filter_by(code_id=patient_file.code_id).first().color
    user = User.query.filter_by(user_id=patient.user_id).first()
    p = PatFile(user.last_name + ' ' + user.first_name, user.birthday, patient.cnp, "Str. Fizicienilor", user.phone, user.email, user.gender, color, patient_file.observations, patient_file.treatment)
    form = PatientFileForm(obj=p)
    if form.validate_on_submit():
        patient_file.observations = form.observatii.data
        patient_file.treatment = form.tratament.data
        codeid = Code.query.filter_by(color=form.cod_urgenta.data).first().code_id
        patient_file.code_id = codeid
        db.session.commit()
        return redirect(url_for('main.user_doctor'))
    return render_template('consulta.html', form=form)


@main.route('finalizeaza/<int:file_id>', methods=["GET", "POST"])
def finalizeaza(file_id):
    user = User.get_by_username(current_user.username)
    patient_file = PatientFile.query.filter_by(file_id=file_id).first()
    patient_file.end_time = datetime.now()
    patient_file.status = 1
    db.session.commit()
    patients = []
    patient_files = PatientFile.query.filter_by(status=0,
                                                attached_unit=1
                                                )
    for x in patient_files:
        color = Code.query.filter_by(code_id=x.code_id).first().color
        userid = Patient.query.filter_by(patient_id=x.patient_id).first().user_id
        user1 = User.query.filter_by(user_id=userid).first()
        name = user1.last_name + ' ' + user1.first_name
        patient = Pats(name, x.file_id, x.patient_id, color)
        patients.append(patient)
        return redirect(url_for('main.user_doctor'))
    return render_template('doctorHome.html', user=user, patients=patients)


@main.route('ambulanceFinalizeaza/<int:file_id>', methods=["GET", "POST"])
def ambulance_finalizeaza(file_id):
    form = AmbulancePacients()
    #user = User.get_by_username(current_user.username)
    patient_file = PatientFile.query.filter_by(file_id=file_id).first()
    patient_file.end_time = datetime.now()
    patient_file.status = 1
    db.session.commit()
    patients = []
    patient_files = PatientFile.query.filter_by(status=0,
                                                attached_unit=0
                                                )
    for x in patient_files:
        color = Code.query.filter_by(code_id=x.code_id).first().color
        userid = Patient.query.filter_by(patient_id=x.patient_id).first().user_id
        user1 = User.query.filter_by(user_id=userid).first()
        name = user1.last_name + ' ' + user1.first_name
        patient = Pats(name, x.file_id, x.patient_id, color)
        patients.append(patient)
        return redirect(url_for('main.ambulance_patient_list'))
    return render_template('ambulancePatientList.html', form=form, user=current_user, patients=patients)


@main.route('mobileHome', methods=["GET", "POST"])
def mobile_home():
    return render_template('mobileHome.html')

@main.route('mobileEstimari', methods=["GET", "POST"])
def mobile_estimari():
    spitale = []
    hospitals = Hospital.query
    for s in hospitals:
        waiting_time = 0
        fise = PatientFile.query.filter_by(hospital_id=s.hospital_id)
        for f in fise:
            waiting_time += Code.query.filter_by(code_id=f.code_id).first().waiting_time
        spital = Spital(s.name, waiting_time, s.hospital_id)
        spitale.append(spital)
    print spitale
    return render_template('mobileEstimari.html', spitale=spitale)

@main.route('mobileCerereInregistrata', methods=["GET", "POST"])
def mobile_cerere_inreg():
    return render_template('mobileCerereInregistrata.html')

@main.route('mobileCerereUPU', methods=["GET", "POST"])
def mobile_login():
    form = CerereUPU()
    if form.validate_on_submit():
        codeid = Code.query.filter_by(color=form.cod_urgenta.data).first().code_id
        patientid = Patient.query.filter_by(user_id=current_user.user_id).first().patient_id
        files = PatientFile.query
        for f in files:
            if f.patient_id == patientid:
                f.code_id = codeid
                f.observations += 'Update de la pacient: ' + form.simptome.data + '; '
                db.session.commit()
                return redirect(url_for('main.mobile_estimari'))
        patientFile = PatientFile(patient_id=patientid,
                                  code_id=codeid,
                                  hospital_id=1,
                                  attached_unit=1,
                                  status=0,
                                  treatment='Pending',
                                  observations='Simptome declarate de pacient: ' + form.simptome.data + '; ')
        db.session.add(patientFile)
        db.session.commit()
        return redirect(url_for('main.mobile_estimari'))
    else:
        flash("Date invalide!")
    return render_template('mobileCerereUPU.html', form=form)


@main.route("mobileSchimbaParola", methods=["GET", "POST"])
def mob_schimba_parola():
    form = SchimbaParola()
    if form.validate_on_submit():
        if form.salveaza.data:
            # Find user - it's current_user
            user = User.query.filter_by(user_id=current_user.user_id).first()
            if User.check_password(user, form.parola_veche.data):
                print 'OK'
                if form.parola_noua.data == form.reintroduceti_parola.data:
                    # Set the new password
                    user.password = form.parola_noua.data
                    db.session.commit()
                    # Redirect to the login page for the user to login with the new password
                    logout_user()
                    return redirect(url_for('main.autentificare'))
                else:
                    flash("Parola reintrodusa nu coincide cu cea de mai sus!")
            else:
                flash("Ati introdus parola veche gresit!")
    return render_template("mobileSchimbaParola.html", form=form)

@main.route('mobileDatePersonale', methods=["GET", "POST"])
def mobile_date_pers():
    form = DatePersonaleForm()
    return render_template('mobileDatePersonale.html', form=form)

@main.route('mobileInregistrare', methods=["GET", "POST"])
def mobile_inregistrare():
    form = MobileInregistrareForm()
    if form.validate_on_submit():
        existingPatient = Patient.query.filter_by(cnp=form.cnp.data).first()
        if existingPatient is None:
            user = User(username=form.cnp.data,
                        first_name=form.nume.data,
                        last_name='',
                        email=form.email.data,
                        birthday=datetime(1985, 3, 27),
                        gender=form.sex.data,
                        type=0,
                        phone=form.telefon.data,
                        password=form.parola.data)
            db.session.add(user)
            db.session.commit()
            userid = User.query.filter_by(username=form.cnp.data).first().user_id
            patient = Patient(user_id=userid,
                              cnp=form.cnp.data)
            db.session.add(patient)
            db.session.commit()
            return redirect(url_for('main.mobile_home'))
        else:
            flash("Aveti deja un cont inregisrat!")
    else:
        flash("Date invalide!")
    return render_template('mobileInregistrare.html', form=form)

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
    print current_user
    #user = User.query.filter_by(user_id=current_user.user_id).first()
    patients = []
    #change the unit to 0
    patient_files = PatientFile.query.filter_by(status=0,
                                                attached_unit=0
                                                )
    for x in patient_files:
        color = Code.query.filter_by(code_id=x.code_id).first().color
        userid = Patient.query.filter_by(patient_id=x.patient_id).first().user_id
        user1 = User.query.filter_by(user_id=userid).first()
        name = user1.last_name + ' ' + user1.first_name
        patient = Pats(name, x.file_id, x.patient_id, color)
        patients.append(patient)
    for y in patients:
        print y.name + "-------------------"
    return render_template('ambulancePatientList.html', form=form, user=current_user, patients=patients)

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
        return redirect(url_for("main.recuperare_cont"))
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
                if user.type == 1:
                    return redirect(url_for('main.user_doctor', user=user))
                elif user.type == 3:
                    return redirect(url_for('main.erHome'))
                    pass
                elif user.type == 2:
                    return redirect(url_for('main.ambulance_home'))
                    pass
                elif user.type == 0:
                    return redirect(url_for('main.mobile_home'))
                flash("Autentifcare reusita pentru utilizatorul: {}.".format(user.username))
            else:
                flash("Date incorecte")
    return render_template('autentificare.html', form=form)



@main.route("inregistrareDoctorER", methods=["GET", "POST"])
def inregistrareDoctorER():
    form = InregistrareDoctorER()
    if form.validate_on_submit():
        nume = form.nume.data
        prenume = form.prenume.data

        data_nasterii = form.data_nasterii.data
        sex = form.sex.data
        spital_partener = form.spital_partener.data
        adresa = form.adresa.data
        nr_telefon = form.nr_telefon.data
        email = form.email.data
        flash(sex)
        flash(form.tip_cont.data)

        username = nume + prenume
        flash(username)

        # Medic: 1, ER: 2
        if form.tip_cont.data == "1":
            flash("Medic")
            type = 1
        elif form.tip_cont.data == "2":
            flash("ER")
            type = 3
        else:
            flash("Alegeti un tip de cont")
            return redirect(url_for('main.inregistrareDoctorER'))
        existingUser = User.query.filter_by(username=username).first()
        if existingUser is None:
            user = User(username=username,
                        first_name=nume,
                        last_name='',
                        email=email,
                        birthday= datetime(1985, 3, 27),
                        gender=sex,
                        type=type,
                        phone=nr_telefon,
                        password='er')
            db.session.add(user)
            db.session.commit()
            flash("Inregistrare reusita!")
        else:
            flash("User deja inregisrat!")
        return redirect(url_for('main.inregistrareDoctorER')) #????????????????????????
    return render_template("inregistrareDoctorER.html", form=form)


@main.route("deconectare")
def deconectare():
    logout_user()
    return render_template("index.html")


@main.route("user_doctor", methods=["GET", "POST"])
def user_doctor():
    user = User.get_by_username(current_user.username)
    patients = []
    patient_files = PatientFile.query.filter_by(status=0,
                                                attached_unit=1
                                                )
    for x in patient_files:
        color = Code.query.filter_by(code_id=x.code_id).first().color
        userid = Patient.query.filter_by(patient_id=x.patient_id).first().user_id
        user1 = User.query.filter_by(user_id=userid).first()
        name = user1.last_name + ' ' + user1.first_name
        patient = Pats(name, x.file_id, x.patient_id, color)
        patients.append(patient)
    for y in patients:
        print y.name + "-------------------"
    return render_template("doctorHome.html", user=user, patients=patients)

@main.route("recuperare_cont", methods=["GET", "POST"])
def recuperare_cont():
    form = RecuperareContForm()
    if form.trimite_cod.data:
        if form.email.data:
            trimis_la = "la adresa de e-mail indicata"
        else:
            trimis_la = "la numarul de telefon indicat"
        flash("Codul a fost trimis {}.".format(trimis_la))
    return render_template("recuperare_cont.html", form=form)

@main.route("schimba_parola", methods=["GET", "POST"])
def schimba_parola():
    form = SchimbaParola()
    return render_template("schimba_parola.html", form=form)