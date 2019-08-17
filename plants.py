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
		cursor.execute("SELECT * FROM plant ORDER BY cast(name as unsigned) ASC")
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
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM plant WHERE id=%s", (id,))
		conn.commit()
		row = cursor.fetchone()
		print(row)

		cursor.execute("SELECT MAX( logdate ) as logdate, stage	FROM log WHERE plant_ID =%s	GROUP BY stage ORDER BY logdate", (id,))
		conn.commit()
		rows = cursor.fetchall()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	return render_template("plants.html",row=row,rows=rows,is_login=session.get('logged_in'))
