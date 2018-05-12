from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, SubmitField, RadioField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,\
    ValidationError


class ContactForm(Form):
    nume = StringField('Nume ', validators=[DataRequired()])
    email = StringField('Email ',validators=[DataRequired(), Length(1, 120), Email()])
    subiect = StringField('Subiect ', validators=[DataRequired()])
    mesaj = TextAreaField('Mesaj ',  validators=[Length(max=200)])
    trimite = SubmitField('Trimite ')


class PatientFileForm(Form):
    nume = StringField('Nume ', validators=[DataRequired()])
    datanasterii = DateTimeField('Data nasterii ', validators=[DataRequired()])
    cnp = StringField('CNP ', validators=[DataRequired()])
    adresa = StringField('Adresa ',  validators=[Length(max=200)])
    telefon = StringField('Telefon ', validators=[Length(max=10)])
    email = StringField('Email ',  validators=[DataRequired(), Length(1, 120), Email()])
    genders = [(x, x) for x in ["Feminin", "Masculin"]]
    sex = RadioField('Sex', choices=genders)
    coduri = ["Rosu", "Galben", "Verde", 'Albastru', "Alb"]
    cod_urgenta = SelectField('Cod urgenta ', choices=coduri, validators=[DataRequired()])
    observatii = TextAreaField('Observatii ',  validators=[Length(max=500)])
    tratament = TextAreaField('Tratament ',  validators=[Length(max=500)])
    adauga = SubmitField('Adauga ')


class AutentificareForm(Form):
    nume = StringField('Nume ', validators=[DataRequired()])
    parola = PasswordField('Parola ', validators=[DataRequired()])
    intra_in_cont = SubmitField('Intra in cont ')
    forgot_password = SubmitField('Ai uitat parola? ')
    files = [(x, x) for x in ["Medic", "ER", "Ambulanta", "Pacient"]]
    tip_cont = RadioField('Tip cont:', choices=files)
    remember_me = BooleanField('Salveaza detalii autentifcare')


class RecuperareContForm(Form):
    telefon = StringField('Telefon')
    email = StringField('E-mail ',validators=[DataRequired(), Length(1, 120), Email()])
    trimite_cod = SubmitField('Timite cod ')


class AmbulanceForgotPassForm(Form):
    oldPassword = StringField('Old Password ', validators=[DataRequired()])
    newPassword = StringField('New Password ', validators=[DataRequired()])
    repeatNewPassword = StringField('Repeat New Password ', validators=[DataRequired()])
    salveaza = SubmitField('Salveaza')


class AmbulanceRegisterPacient(Form):
    register = SubmitField('Inregistreaza pacient')


class AmbulancePacients(Form):
    pacient = StringField('', validators=[DataRequired()])
    search = SubmitField('Cauta pacient')
    transfera = SubmitField('Transfera pacienti')