from wtforms import Form, TextField, SelectField, TextAreaField, DateField, validators, StringField, SubmitField
from pytz import all_timezones
import pymysql
from db_config import mysql

def get_db_list(table):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM %s" % table)
        rows = cursor.fetchall()
        results = [('Unknown','Unknown')]
        for row in rows:
        	results.append((str(row['name']),row['name']))
        #print("RES:",results)
        return results
    except Exception as e:
        print(e)

class SettingsForm(Form):
    timezone_choices = []
    for tz in all_timezones:
        timezone_choices.append((tz,tz))
    #print(timezone_choices)
    timezone = SelectField('Timezone:',choices=timezone_choices)
    temp = SelectField('Temperature:', choices=[('C','Celsius'),('F','Farenheit'),('K','Kelvin')])
    length = SelectField('Length:',choices=[('cm','Centimeters'),('in','Inches')])
    volume = SelectField('Volume:',choices=[('ml','Mililiters'),('oz','Ounces')])
    date_format = TextField('Date Format:')

class PlantForm(Form):
    strains = get_db_list('strain')
    seasons = get_db_list('season')

    name = TextField('Name:', validators=[validators.required()])
    gender = SelectField('Gender:',choices=[('unknown','Unknown'),('male','Male'),('female','Female'),('hermaphrodite','Hermaphrodite')])
    strain = SelectField('Strain:',choices=strains)
    season = SelectField('Season:',choices=seasons)
    source = SelectField('Source:',choices=[('seed','Seed'),('clone','Clone'),('other','Other')])

class SeasonForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    start = DateField('Start:', validators=[validators.required()])
    end = DateField('End:')
    location = TextField('Location:')
    light_hours = TextField('Light Hours:')

class StrainForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    type = SelectField('Type:',choices=[('unknown','Unknown'),('indica','Indica'),('sativa','Sativa'),('ruderalis','Ruderalis'),('blend','Blend')])
    notes = TextAreaField('Notes')

class EnvironmentForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    location = SelectField('Location:',choices=[('indoor','Indoor'),('outdoor','Outdoor')])
    light_hours = TextField('Light Hours:')

class NutrientForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    organic = SelectField('Organic:',choices=[('yes','Yes'),('no','No')])
    nitrogen = TextField('Nitrogen:')
    phosphorus = TextField('Phosphorus:')
    potassium = TextField('Potassium:')
    trace = TextField('Trace:')

class RepellentForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    type = SelectField('Type:',choices=[('organic','Organic'),('chemical','Chemical'),('other','Other')])
    target = TextField('Target:')
    notes = TextAreaField('Notes')
