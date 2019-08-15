from flask_table import Table, Col, LinkCol
from wtforms import Form, TextField, SelectField, TextAreaField, validators, StringField, SubmitField
from pytz import all_timezones
import pymysql
from db_config import mysql

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
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM strain")
    rows = cursor.fetchall()
    strains = []
    for row in rows:
    	strains.append((row['name'],row['name']))
    cursor.execute("SELECT * FROM season")
    rows = cursor.fetchall()
    seasons = []
    for row in rows:
    	seasons.append((row['name'],row['name']))

    name = TextField('Name:', validators=[validators.required()])
    gender = SelectField('Gender:',choices=[('unknown','Unknown'),('male','male'),('female','Female'),('hermaphrodite','Hermaphrodite')])
    strain = SelectField('Strain:',choices=strains)
    season = SelectField('Season:',choices=seasons)


class Plant(Table):
    id = Col('id', show=False)
    name = Col('Name')
    gender = Col('Gender')
    strain_ID = Col('Strain')
    season_ID = Col('Season')
    edit = LinkCol('Edit', 'edit_plant', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_plant', url_kwargs=dict(id='id'))
