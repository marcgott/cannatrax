from flask_table import Table, Col, LinkCol, ButtonCol, BoolNaCol, DateCol

class Plant(Table):
    classes = ['main','chart','plant']
    id = Col('id', show=False)
    name = Col('Name')
    gender = Col('Gender')
    strain_ID = Col('Strain')
    season_ID = Col('Season')
    source = Col('Source')
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
    notes = Col('Notes')
    edit = LinkCol('Edit', 'edit_repellent', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_repellent', url_kwargs=dict(id='id'))

class Statistics(Table):
    classes = ['statistics']
    pc = Col('Plant Count')
    ec = Col('Environment Count')
    sc = Col('Strain Count')
    ac = Col('Season Count')
    rc = Col('Repellent Count')
    nc = Col('Nutrient Count')
    lastlog = DateCol('Last Log')
