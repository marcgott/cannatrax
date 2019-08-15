#! /usr/bin/env python3.5

import pymysql
from app import app
#from flask_table import Table
from db_config import mysql
from flask import flash, render_template, request, redirect
from wtforms import Form, TextField, SelectField, TextAreaField, validators, StringField, SubmitField
from tables import *
from forms import *

icon="home"
#
# Show default environments page, general statistics
@app.route('/environments')
def show_environments():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM environment ORDER BY name ASC")
		rows = cursor.fetchall()
		table = Environment(rows)
		table.border = True
		total_environments = len(rows)
		return render_template('environments.html', table=table, total_environments=total_environments)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

#
# Display and process new environment
@app.route('/environment/new', methods=['GET','POST'])
def add_new_environment_view():
	icon=None
	if request.method == 'POST':
		try:
			_name = request.form['name']
			_location = request.form['location']
			_light_hours = request.form['light_hours']

			sql = "INSERT INTO environment(name,location,light_hours) VALUES(%s, %s, %s)"
			data = (_name, _location, _light_hours)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			icon="home"
			flash('New Environment Added!','info')
		except Exception as e:
			icon="remove"
			flash('New environment Not Added!','error')
			print(e)

	try:
		form = EnvironmentForm(request.form)
	except Exception as e:
		print(e)
	title_verb = "Add"
	return render_template('add_environment.html', title_verb=title_verb, form=form, icon=icon, row=None)

@app.route('/environment/edit/<int:id>', methods=['POST','GET'])
def edit_environment(id):
	icon=None
	if request.method == "POST":
		_name = request.form['name']
		_location = request.form['location']
		_light_hours = request.form['light_hours']
		_id = request.form['id']

		sql = "UPDATE environment SET name=%s, location=%s, light_hours=%s WHERE id=%s"
		data = (_name, _location, _light_hours, _id)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql, data)
		conn.commit()
		icon="home"
		flash('environment updated successfully!','info')

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM environment WHERE id=%s", id)
		row = cursor.fetchone()

		if row:
			form = EnvironmentForm(request.form)
			form.name.default=row['name']
			form.location.default=row['location']
			form.light_hours.default=row['light_hours']
			form.process()
		else:
			return 'Error loading #{id}'.format(id=id)
		title_verb = "Edit"

		return render_template('add_environment.html', title_verb=title_verb, icon=icon, form=form, row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/environment/delete/<int:id>')
def delete_environment(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM environment WHERE id=%s", (id,))
		conn.commit()
		flash('environment deleted successfully!','info')
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	return redirect("/environments")
