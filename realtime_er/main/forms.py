from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,\
    ValidationError


class ContactForm(Form):
    nume = StringField('Nume ', validators=[DataRequired()])
    email = StringField('Email ',validators=[DataRequired(), Length(1, 120), Email()])
    subiect = StringField('Subiect ', validators=[DataRequired()])
    mesaj = TextAreaField('Mesaj ',  validators=[Length(max=200)])
    trimite = SubmitField('Trimite ')