from wtforms import Form, HiddenField, TextField, PasswordField, SelectField, TextAreaField, DateField, BooleanField, IntegerField, validators, StringField, SubmitField
from pytz import all_timezones
import pymysql
from db_config import mysql

def get_db_list(**kwargs):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM %s" % kwargs['table'])
        rows = cursor.fetchall()
        optval = 0 if kwargs['idval'] == True else "Unknown"
        opttxt = kwargs['idtxt'] if kwargs['idtxt'] is not None else "Unknown"

        results = [(optval,opttxt)]
        for row in rows:
        	optval = row['id'] if kwargs['idval'] == True else row['name']
        	results.append((str(optval),row['name']))
        return results
    except Exception as e:
        print(e)

class LoginForm(Form):
    username = TextField("Username")
    password = PasswordField("Password")

class SettingsForm(Form):
    timezone_choices = []
    for tz in all_timezones:
        timezone_choices.append((tz,tz))
    #print(timezone_choices)
    username = TextField('Username:')
    password = TextField('Password:')
    timezone = SelectField('Timezone:',choices=timezone_choices)
    temp_units = SelectField('Temperature:', choices=[('C','Celsius'),('F','Farenheit'),('K','Kelvin')])
    length_units = SelectField('Length:',choices=[('cm','Centimeters'),('in','Inches')])
    volume_units = SelectField('Volume:',choices=[('ml','Mililiters'),('oz','Ounces')])
    date_format = SelectField('Date Format:', choices=[('yyyy-mm-dd','yyyy-mm-dd'),('mm/dd/yyyy','mm/dd/yyyy')])

class PlantForm(Form):
    strains = get_db_list(table='strain',idval = True,idtxt = "Unknown")
    seasons = get_db_list(table='season',idval = True,idtxt = "Unknown")
    name = TextField('Name:', validators=[validators.required()])
    gender = SelectField('Gender:',choices=[('Unknown','Unknown'),('Male','Male'),('Female','Female'),('Hermaphrodite','Hermaphrodite')])
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
    price = TextField('Price:')
    purchase_location = TextField('Purchase Location:')
    notes = TextAreaField('Notes')

class LogForm(Form):
    environment = get_db_list(table = 'environment',idval = True,idtxt = "None")
    nutrient = get_db_list(table = 'nutrient',idval = True,idtxt = "None")
    repellent = get_db_list(table = 'repellent',idval = True,idtxt = "None")
    logdate = DateField('Date')
    plant_ID = HiddenField()
    water = BooleanField('Water')
    height = IntegerField('Height')
    span = IntegerField('Span')
    trim = BooleanField('Trim')
    transplant = BooleanField('Transplant')
    stage = SelectField('Stage',choices=[('Germination','Germination'),('Seedling','Seedling'),('Vegitation','Vegitation'),('Pre-Flowering','Pre-Flowering'),('Flowering','Flowering'),('Harvest','Harvest'),('Archive','Archive'),('Dead','Dead')])
    environment_ID = SelectField('Environment',choices=environment, coerce=int)
    nutrient_ID = SelectField('Nutrient',choices=nutrient, coerce=int)
    repellent_ID = SelectField('Repellent',choices=repellent, coerce=int)
    notes = TextAreaField('Notes')
