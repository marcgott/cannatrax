#! /usr/bin/env python3.5

import pymysql
from app import app
from db_config import mysql
from werkzeug import generate_password_hash, check_password_hash
from flask import flash, render_template, request, redirect,session, abort
from pytz import all_timezones
import json
from forms import *
from tables import *
from plants import *
from cycles import *
from strains import *
from environments import *
from nutrients import *
from repellents import *
from reports import *
from log import *
from api import *

#app.secret_key = generate_password_hash('cannatrax')
app.secret_key = "cannatrax"
app.settings = {}
app.program_name="CannaTrax"
app.settings = get_settings()

try:
	from db_config import mysql
except Exception as e:
	print(e)
	from install import *

@app.route('/')
def show_menu():
	if not session.get('logged_in'):
		form = LoginForm(request.form)
		referrer = request.headers.get("Referer")
		return render_template('login.html',referrer=referrer,form=form,program_name=program_name,operation="Log In",is_login=session.get('logged_in'))
	operation="Dashboard"
	try:
		countsql = "SELECT (SELECT count(plant.id) FROM `plant` WHERE plant.current_stage NOT IN ('Archive','Dead')) as 'pc' ,(SELECT count(environment.id) FROM `environment`) as 'ec', (SELECT count(strain.id) FROM `strain`) as 'sc', (SELECT count(cycle.id) FROM `cycle`) as 'ac', (SELECT count(repellent.id) FROM `repellent`) as 'rc', (SELECT count(nutrient.id) FROM `nutrient`) as 'nc', (SELECT max(log.ts) FROM `log`) as 'lastlog'"
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(countsql)
		rows = cursor.fetchall()
		table = Statistics(rows)

		countsql = "SELECT * FROM options"
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(countsql)
		rows = cursor.fetchall()
		settings_list = []
		settings = {}
		for row in rows:
			settings[row['option_key']] = row['option_value']
		settings_list.append(settings)
		settings_table = Settings(settings_list)
		day = json.loads(get_daystats())
		session['daylight'] = day['results']['day_length']
		format = '%H:%M:%S'
		midnight = "23:59:59"
		darkness = datetime.strptime(midnight, format) - datetime.strptime(session['daylight'], format)
		session['darkness'] = str(darkness)
		icon="tachometer-alt"
		return render_template('dashboard.html', day=day['results'], icon=icon, table=table, program_name=app.program_name, settings_table=settings_table,settings=settings,operation=operation,is_login=session.get('logged_in'))
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/login', methods=['POST'])
def do_admin_login():
	option = get_settings();
	try:
		if request.form['password'] == option['password'] and request.form['username'] == option['username']:
			session['logged_in'] = True
			flash('Successful Login', 'info')
			redirect_url = request.form['redirect'] if "redirect" in request.form !='' else "/"
	except Exception as e:
		ptint(e)
		flash('wrong password!')
	finally:
		return redirect("/")


@app.route('/logout', methods=['GET','POST'])
def do_logout():
	session['logged_in'] = False
	return redirect("/")

@app.route('/settings')
def show_settings():
	if check_login() is not True:
		return redirect("/")
	operation="Settings"
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM options")
		rows = cursor.fetchall()
		if rows:
			form = SettingsForm(request.form)
			for row in rows:
				key = row['option_key']
				value = row['option_value']
				opt = getattr(form,key)
				setattr(opt,'default',value)
			form.process()
		icon="bars"
		return render_template('operation_form.html', formpage='settings.html', icon=icon,form=form,operation=operation,is_login=session.get('logged_in'))
	except Exception as e:
			print(e)

@app.route('/settings/update', methods=['POST'])
def update_user():
	global app
	try:
		_username = request.form['username']
		_password = request.form['password']
		_date_format = request.form['date_format']
		_timezone = request.form['timezone']
		_temp_units = request.form['temp_units']
		_length_units = request.form['length_units']
		_volume_units = request.form['volume_units']
		_latitude = request.form['latitude']
		_longitude = request.form['longitude']
		_allow_plantlog_edit = "True" if 'allow_plantlog_edit' in request.form else ""
		_allow_envlog_edit = "True" if 'allow_envlog_edit' in request.form else ""
		# validate the received values

		sql = "UPDATE options SET `option_value`=%s WHERE `option_key`='timezone'; UPDATE options SET `option_value`=%s WHERE `option_key`='temp_units'; UPDATE options SET `option_value`=%s WHERE `option_key`='length_units'; UPDATE options SET `option_value`=%s WHERE `option_key`='volume_units'; UPDATE options SET `option_value`=%s WHERE `option_key`='date_format';UPDATE options SET `option_value`=%s WHERE `option_key`='username';UPDATE options SET `option_value`=%s WHERE `option_key`='password';UPDATE options SET `option_value`=%s WHERE `option_key`='allow_plantlog_edit';UPDATE options SET `option_value`=%s WHERE `option_key`='allow_envlog_edit';UPDATE options SET `option_value`=%s WHERE `option_key`='latitude';UPDATE options SET `option_value`=%s WHERE `option_key`='longitude'; "
		data = (_timezone, _temp_units, _length_units, _volume_units, _date_format, _username, _password,_allow_plantlog_edit,_allow_envlog_edit,_latitude,_longitude)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql, data)
		conn.commit()
		flash('Settings updated successfully!','info')
		app.settings = get_settings()
		return redirect('/settings')
	except Exception as e:
		icon="times-circle"
		flash('Settings not updated','error')
		print(e)
		return redirect('/settings')

	finally:
		pass
		#cursor.close()
		#conn.close()

if __name__ == "__main__":
    app.run(use_reloader=True, debug=False, host='0.0.0.0', port=4200)
