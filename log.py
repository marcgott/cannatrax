#! /usr/bin/env python3.5

import pymysql
from app import app
#from flask_table import Table
from db_config import mysql
from flask import flash, render_template, request, redirect, session
from wtforms import Form, TextField, SelectField, TextAreaField, validators, StringField, SubmitField
from tables import *
from forms import *

icon="clipboard-check"
operation="Log"
#
# Show default logs page, general statistics
@app.route('/logs')
def show_logs():
	if check_login() is not True:
		return redirect("/")
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT log.*, plant.name as plant_name, nutrient.name as nutrient_name, environment.name as environment_name, repellent.name as repellent_name FROM log LEFT JOIN plant ON plant.id = log.plant_ID LEFT JOIN nutrient ON nutrient.id = log.nutrient_ID LEFT JOIN environment ON environment.id = log.environment_ID LEFT JOIN repellent ON repellent.id = log.repellent_ID ORDER BY logdate DESC, ts DESC LIMIT 40")
		rows = cursor.fetchall()
		table = Log(rows)
		table.border = True
		total_logs = len(rows)
		#icon="clipboard-check"
		return render_template('logs.html', table=table, icon=icon, total_logs=total_logs,operation=operation,is_login=session.get('logged_in'))
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/log/print', methods=['GET'])
def add_print_log_view():
	if check_login() is not True:
		return redirect("/")
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT name FROM plant ORDER BY CAST(name AS unsigned)")
		rows = cursor.fetchall()
		tablerows = []
		option = get_settings()
		for row in rows:
			printrow = {}
			printrow['name'] = row['name']
			printrow['picture']= ''
			printrow['water']= ''+option['volume_units']
			printrow['nutrient']= ''
			printrow['height']= ''+option['length_units']
			printrow['span']= ''+option['length_units']
			printrow['transplant']= ''
			printrow['lux']= ''
			printrow['soil_pH']= ''
			printrow['trim']= ''
			printrow['notes']= ''
			tablerows.append(printrow)
		table = PrintLog(tablerows)
		table.border = True
	except Exception as e:
		print(e)
	title_verb = "Print"
	icon="clipboard-check"
	return render_template('print_log.html', title_verb=title_verb, table=table, icon=icon, rows=rows,operation=operation,is_login=session.get('logged_in'))

#
# Display and process new log
@app.route('/log/new', methods=['GET','POST'])
def add_new_log_view():
	if check_login() is not True:
		return redirect("/")
	icon=None
	if request.method == 'POST':
		try:
			_water = 1 if 'water' in request.form else 0
			_transplant = 1 if 'transplant' in request.form else 0
			_plant_ID = request.form['plant_ID']
			_height = request.form['height']
			_span = request.form['span']
			_environment_ID = request.form['environment_ID']
			_nutrient_ID = request.form['nutrient_ID']
			_repellent_ID = request.form['repellent_ID']
			_stage = request.form['stage']
			_lux = request.form['lux']
			_soil_pH = request.form['soil_pH']
			_logdate = request.form['logdate']
			_trim = request.form['trim']
			_notes = request.form['notes']

			sql = "INSERT INTO log(plant_ID, water, height, span, environment_ID, nutrient_ID, repellent_ID, stage, trim, transplant, notes, logdate, lux, soil_pH ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			data = (_plant_ID, _water, _height, _span, _environment_ID, _nutrient_ID, _repellent_ID, _stage, _trim, _transplant, _notes, _logdate, _lux, _soil_pH)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()

			sql = "UPDATE plant set current_stage=%s , current_environment=%s WHERE id=%s"
			data = (_stage,_environment_ID, _plant_ID)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()

			icon="clipboard-check"
			flash('New Log Added!','info')
		except Exception as e:
			icon="remove"
			flash('New Log Not Added','error')
			print(e)

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT id,name FROM plant ORDER BY CAST(name AS unsigned)")
		rows = cursor.fetchall()
		form = LogForm(request.form)
	except Exception as e:
		print(e)
	title_verb = "Add"
	icon="clipboard-check"
	icons = get_icons()
	return render_template('operation_form.html', formpage='add_log.html', title_verb=title_verb, form=form, icon=icon, icons=icons, rows=rows,operation=operation,is_login=session.get('logged_in'))

@app.route('/log/edit/<int:id>', methods=['POST','GET'])
def edit_log(id):
	icon=None
	if request.method == "POST":
		_name = request.form['name']
		_gender = request.form['gender']
		_strain = request.form['strain']
		_cycle = request.form['cycle']
		_source = request.form['source']
		_id = request.form['id']

		sql = "UPDATE log SET name=%s, gender=%s, strain_ID=%s, cycle_ID=%s, source=%s WHERE id=%s"
		data = (_name, _gender, _strain, _cycle, _source, _id)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql, data)
		conn.commit()
		icon="clipboard-check"
		flash('Log updated successfully!','info')

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM log WHERE id=%s", id)
		row = cursor.fetchone()

		if row:
			form = LogForm(request.form)
			form.name.default=row['name']
			form.gender.default=row['gender']
			form.source.default=row['source']
			form.strain.default=row['strain_ID']
			form.cycle.default=row['cycle_ID']

			form.process()
		else:
			return 'Error loading #{id}'.format(id=id)
		title_verb = "Edit"
		icon="clipboard-check"
		return render_template('operation_form.html', formpage='add_log.html', title_verb=title_verb, icon=icon, form=form, row=row, rowid=row['id'],operation=operation,is_login=session.get('logged_in'))
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/log/delete/<int:id>')
def delete_log(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM log WHERE id=%s", (id,))
		conn.commit()
		flash('Log deleted successfully!','info')
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	return redirect("/logs")
