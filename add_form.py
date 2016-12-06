# from flask_wtf import Form
from wtforms import Form, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, StringField, validators, ValidationError

class Add_Asset_Form(Form):

    city = TextField("city", [validators.DataRequired()])
    contact = TextField("contact", [validators.DataRequired()])
    descript = TextField("descript", [validators.DataRequired()])
    idcode = TextField("id", [validators.DataRequired()])
    lat = TextField("lat")
    lon = TextField("lon")
    name = TextField("name", [validators.DataRequired()])
    state = TextField("state", [validators.DataRequired()])
    street = TextField("street", [validators.DataRequired()])
    telnum = TextField("telnum", [validators.DataRequired()])
    website = TextField("website")
    zipcode = TextField("zip", [validators.DataRequired()])
