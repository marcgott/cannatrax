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
		cursor.execute("SELECT log.*, plant.name as plant_name, nutrient.name as nutrient_name, environment.name as environment_name, repellent.name as repellent_name FROM log LEFT JOIN plant ON plant.id = log.plant_ID LEFT JOIN nutrient ON nutrient.id = log.nutrient_ID LEFT JOIN environment ON environment.id = log.environment_ID LEFT JOIN repellent ON repellent.id = log.repellent_ID ORDER BY logdate DESC LIMIT 20")
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

#
# Display and process new log
@app.route('/log/new', methods=['GET','POST'])
def add_new_log_view():
	icon=None
	if request.method == 'POST':
		try:
			_water = 1 if 'water' in request.form else 0
			_trim = 1 if 'trim' in request.form else 0
			_transplant = 1 if 'transplant' in request.form else 0
			_plant_ID = request.form['plant_ID']
			_height = request.form['height']
			_span = request.form['span']
			_environment_ID = request.form['environment_ID']
			_nutrient_ID = request.form['nutrient_ID']
			_repellent_ID = request.form['repellent_ID']
			_stage = request.form['stage']
			_notes = request.form['notes']

			sql = "INSERT INTO log(plant_ID, water, height, span, environment_ID, nutrient_ID, repellent_ID, stage, trim, transplant, notes ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			data = (_plant_ID, _water, _height, _span, _environment_ID, _nutrient_ID, _repellent_ID, _stage, _trim, _transplant, _notes)
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
		print("refreshing")
		rows = cursor.fetchall()
		form = LogForm(request.form)
	except Exception as e:
		print(e)
	title_verb = "Add"
	icon="clipboard-check"
	return render_template('operation_form.html', formpage='add_log.html', title_verb=title_verb, form=form, icon=icon, rows=rows,operation=operation,is_login=session.get('logged_in'))

@app.route('/log/edit/<int:id>', methods=['POST','GET'])
def edit_log(id):
	icon=None
	if request.method == "POST":
		_name = request.form['name']
		_gender = request.form['gender']
		_strain = request.form['strain']
		_season = request.form['season']
		_source = request.form['source']
		_id = request.form['id']

		sql = "UPDATE log SET name=%s, gender=%s, strain_ID=%s, season_ID=%s, source=%s WHERE id=%s"
		data = (_name, _gender, _strain, _season, _source, _id)
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
			form.season.default=row['season_ID']

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
