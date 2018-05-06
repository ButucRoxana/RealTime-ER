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
    trimite_cont = SubmitField("Timite cont")