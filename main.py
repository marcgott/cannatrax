#! /usr/bin/env python3.5

import pymysql
from app import app
from db_config import mysql
from flask import flash, render_template, request, redirect
from pytz import all_timezones
from forms import *
from tables import *
from plants import *
from seasons import *
from strains import *
from environments import *
from nutrients import *
from repellents import *

@app.route('/')
def show_menu():
	try:
		countsql = "SELECT (SELECT count(plant.id) FROM `plant`) as 'pc' ,(SELECT count(environment.id) FROM `environment`) as 'ec', (SELECT count(strain.id) FROM `strain`) as 'sc', (SELECT count(season.id) FROM `season`) as 'ac', (SELECT count(repellent.id) FROM `repellent`) as 'rc', (SELECT count(nutrient.id) FROM `nutrient`) as 'nc', (SELECT max(log.ts) FROM `log`) as 'lastlog'"
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(countsql)
		rows = cursor.fetchall()
		table = Statistics(rows)
		return render_template('dashboard.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/settings')
def show_settings():
    form = SettingsForm(request.form)
    return render_template('settings.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
