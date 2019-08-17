from flask_table import Table, Col, LinkCol, ButtonCol, BoolCol, BoolNaCol, DateCol, DatetimeCol
from cannatrax import *

class Log(Table):
    table_id = ['daily_log']
    classes = ['main','chart','log']
    id = Col('id', show=False)
    plant_name = Col('Plant Name')
    logdate = DateCol('Log Date', date_format='medium')
    stage = Col('Stage')
    water = BoolCol('Watered',  yes_display='Yes', no_display='No')
    height = Col('Height')
    span = Col('Span')
    nutrient_name = Col('Nutrient')
    repellent_name = Col('Repellent')
    environment_name = Col('Environment')
    trim = BoolCol('Trim',  yes_display='Yes', no_display='No')
    transplant = BoolCol('Transplant',  yes_display='Yes', no_display='No')
    #edit = LinkCol('Edit', 'edit_plant', url_kwargs=dict(id='id'))
    #delete = LinkCol('Delete', 'delete_plant', url_kwargs=dict(id='id'))

class Plant(Table):
    classes = ['main','chart','plant']
    id = Col('id', show=False)
    name = Col('Name')
    gender = Col('Gender')
    strain_ID = Col('Strain')
    season_ID = Col('Season')
    source = Col('Source')
    details = LinkCol('Details', 'view_plant', url_kwargs=dict(id='id'))
    edit = LinkCol('Edit', 'edit_plant', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_plant', url_kwargs=dict(id='id'))

class Season(Table):
    classes = ['main','chart','season']
    id = Col('id', show=False)
    name = Col('Name')
    start = Col('Start')
    end = Col('End')
    location = Col('Location')
    light_hours = Col('Light Hours')
    edit = LinkCol('Edit', 'edit_season', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_season', url_kwargs=dict(id='id'))

class Strain(Table):
    classes = ['main','chart','strain']
    id = Col('id', show=False)
    name = Col('Name')
    type = Col('Type')
    notes = Col('Notes')
    edit = LinkCol('Edit', 'edit_strain', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_strain', url_kwargs=dict(id='id'))

class Environment(Table):
    classes = ['main','chart','environment']
    id = Col('id', show=False)
    name = Col('Name')
    location = Col('Location')
    light_hours = Col('Light Hours')
    edit = LinkCol('Edit', 'edit_environment', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_environment', url_kwargs=dict(id='id'))

class Nutrient(Table):
    classes = ['main','chart','nutrient']
    id = Col('id', show=False)
    name = Col('Name')
    organic = Col('Organic')
    nitrogen = Col('Nitrogen')
    phosphorus = Col('Phosphorus')
    potassium = Col('Potassium')
    trace = Col('Trace')
    edit = LinkCol('Edit', 'edit_nutrient', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_nutrient', url_kwargs=dict(id='id'))

class Repellent(Table):
    classes = ['main','chart','repellent']
    id = Col('id', show=False)
    name = Col('Name')
    type = Col('Type')
    target = Col('Target')
    price = Col('Price')
    purchase_location = Col('Purchase Location')
    notes = Col('Notes')
    edit = LinkCol('Edit', 'edit_repellent', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_repellent', url_kwargs=dict(id='id'))

class Statistics(Table):
    settings = get_settings()
    table_id = ['statistics']
    classes = ['statistics']
    pc = Col('Plant Count')
    ec = Col('Environment Count')
    sc = Col('Strain Count')
    ac = Col('Season Count')
    rc = Col('Repellent Count')
    nc = Col('Nutrient Count')
    lastlog = DatetimeCol('Last Log')

class Settings(Table):
    table_id = ['settings']
    classes = ['statistics']
    username = Col('Username')
    password = Col('Password', show=False)
    timezone = Col('Timezone')
    temp_units = Col('Temperature Units')
    volume_units = Col('Volume Units')
    length_units = Col('Length_Units')
    date_format = Col('Date Format')
