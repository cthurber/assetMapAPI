# from flask_wtf import Form
from wtforms import Form, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, StringField, validators, ValidationError

class Add_Asset_Form(Form):

    city = TextField("city")
    contact = TextField("contact")
    descript = TextField("descript")
    idcode = TextField("id")
    lat = TextField("lat")
    lon = TextField("lon")
    name = TextField("name")
    state = TextField("state")
    street = TextField("street")
    telnum = TextField("telnum")
    website = TextField("website")
    zipcode = TextField("zip")
