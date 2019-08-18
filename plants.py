#! /usr/bin/env python3.5

import pymysql
from app import app
#from flask_table import Table
from db_config import mysql
from flask import flash, render_template, request, redirect, session
from wtforms import Form, TextField, SelectField, TextAreaField, validators, StringField, SubmitField
from tables import *
from forms import *

operation="Plants"
icon="leaf"

#
# Show default plants page, general statistics
@app.route('/plants')
def show_plants():
	if check_login() is not True:
		return redirect("/")
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT plant.id, plant.name as name, plant.gender, strain.name as strain_name, season.name as season_name,environment.name as current_environment, plant.source, plant.current_stage FROM plant LEFT JOIN strain on strain.id=plant.strain_ID LEFT JOIN season ON season.id=plant.season_ID LEFT JOIN environment ON environment.id=plant.current_environment ORDER BY cast(plant.name as unsigned) ASC")
		rows = cursor.fetchall()
		table = Plant(rows)
		table.border = True
		total_plants = len(rows)
		return render_template('main.html', table=table, total_count=total_plants, add_operation_url='.add_new_plant_view',icon=icon,operation=operation,is_login=session.get('logged_in'))
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

#
# Display and process new plant
@app.route('/plant/new', methods=['GET','POST'])
def add_new_plant_view():
	if check_login() is not True:
		return redirect("/")
	icon=None
	if request.method == 'POST':
		try:
			_name = request.form['name']
			_gender = request.form['gender']
			_strain_ID = request.form['strain']
			_season_ID = request.form['season']
			_source = request.form['source']

			sql = "INSERT INTO plant(name,gender,strain_ID,season_ID,source) VALUES(%s, %s, %s, %s, %s)"
			data = (_name, _gender, _strain_ID, _season_ID, _source)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			icon="leaf"
			flash('New Plant Added!','info')
		except Exception as e:
			icon="remove"
			flash('New Plant Not Added!','error')
			print(e)

	try:
		form = PlantForm(request.form)
	except Exception as e:
		print(e)
	title_verb = "Add"
	return render_template('operation_form.html', formpage='add_plant.html', title_verb=title_verb, form=form, icon=icon, row=None, operation=operation,is_login=session.get('logged_in'))

@app.route('/plant/edit/<int:id>', methods=['POST','GET'])
def edit_plant(id):
	if check_login() is not True:
		return redirect("/")
	icon=None
	if request.method == "POST":
		_name = request.form['name']
		_gender = request.form['gender']
		_strain = request.form['strain']
		_season = request.form['season']
		_source = request.form['source']
		_id = request.form['id']

		sql = "UPDATE plant SET name=%s, gender=%s, strain_ID=%s, season_ID=%s, source=%s WHERE id=%s"
		data = (_name, _gender, _strain, _season, _source, _id)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql, data)
		conn.commit()
		icon="leaf"
		flash('Plant updated successfully!','info')

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM plant WHERE id=%s", id)
		row = cursor.fetchone()

		if row:
			form = PlantForm(request.form)
			form.name.default=row['name']
			form.gender.default=row['gender']
			form.source.default=row['source']
			form.strain.default=row['strain_ID']
			form.season.default=row['season_ID']
			form.process()
		else:
			return 'Error loading #{id}'.format(id=id)
		title_verb = "Edit"

		return render_template('operation_form.html', formpage='add_plant.html', title_verb=title_verb, icon=icon, form=form, row=row, operation=operation,is_login=session.get('logged_in'))
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/plant/delete/<int:id>')
def delete_plant(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM plant WHERE id=%s", (id,))
		conn.commit()
		flash('Plant deleted successfully!','info')
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	return redirect("/plants")

@app.route('/plant/view/<int:id>')
def view_plant(id):
	if check_login() is not True:
		return redirect("/")
	title_verb="View"
	try:
		option = get_settings()
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT plant.id, plant.name as name, plant.gender, strain.name as strain_name, season.name as season_name, plant.source, environment.name as current_environment, plant.current_stage as current_stage, max(log.height) as current_height, max(log.span) as current_span FROM plant LEFT JOIN strain on strain.id=plant.strain_ID LEFT JOIN season ON season.id=plant.season_ID LEFT JOIN environment ON environment.id=plant.current_environment LEFT JOIN log ON plant.id=log.plant_ID WHERE plant.id=%s", (id,))
		conn.commit()
		row = cursor.fetchone()
		cursor.execute("SELECT MAX( logdate ) as logdate, stage	FROM log WHERE plant_ID =%s	GROUP BY stage ORDER BY logdate", (id,))
		conn.commit()
		rows = cursor.fetchall()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	return render_template("plants.html",icon=get_icons(),option=option,row=row,rows=rows,operation=operation,title_verb=title_verb,is_login=session.get('logged_in'))
