#! /usr/bin/env python3.5

from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'cannatrax'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cannatrax'
app.config['MYSQL_DATABASE_DB'] = 'cannatrax'
app.config['MYSQL_DATABASE_HOST'] = '10.100.102.100'
app.config['FA-KIT'] = '61426b7f55'
mysql.init_app(app)
