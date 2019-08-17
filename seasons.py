#! /usr/bin/env python3.5

import pymysql
from app import app
#from flask_table import Table
from db_config import mysql
from flask import flash, render_template, request, redirect, session
from wtforms import Form, TextField, SelectField, TextAreaField, validators, StringField, SubmitField
from tables import *
from forms import *

operation="Seasons"
icon="hourglass"
#
# Show default seasons page, general statistics
@app.route('/seasons')
def show_seasons():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM season ORDER BY name ASC")
		rows = cursor.fetchall()
		table = Season(rows)
		table.border = True
		total_seasons = len(rows)
		return render_template('main.html', table=table, total_count=total_seasons, add_operation_url='.add_new_season_view',icon=icon,operation=operation,is_login=session.get('logged_in'))
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

#
# Display and process new season
@app.route('/season/new', methods=['GET','POST'])
def add_new_season_view():
	icon=None
	if request.method == 'POST':
		try:
			_name = request.form['name']
			_location = request.form['location']
			_start = request.form['start']
			_end = request.form['end']
			_light_hours = request.form['light_hours']

			sql = "INSERT INTO season(name,location,start,end,light_hours) VALUES(%s, %s, %s, %s, %s)"
			data = (_name, _location, _start, _end, _light_hours)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			icon="hourglass"
			flash('New Season Added!','info')
		except Exception as e:
			icon="remove"
			flash('New Season Not Added!','error')
			print(e)

	try:
		form = SeasonForm(request.form)
	except Exception as e:
		print(e)
	title_verb = "Add"
	return render_template('operation_form.html', formpage='add_season.html', title_verb=title_verb, form=form, icon=icon, row=None,operation=operation,is_login=session.get('logged_in'))

@app.route('/season/edit/<int:id>', methods=['POST','GET'])
def edit_season(id):
	icon=None
	if request.method == "POST":
		_name = request.form['name']
		_location = request.form['location']
		_start = request.form['start']
		_end = request.form['end']
		_light_hours = request.form['light_hours']
		_id = request.form['id']

		sql = "UPDATE season SET name=%s, location=%s, start=%s, end=%s, light_hours=%s WHERE id=%s"
		data = (_name, _location, _start, _end, _light_hours, _id)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql, data)
		conn.commit()
		icon="hourglass"
		flash('season updated successfully!','info')

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM season WHERE id=%s", id)
		row = cursor.fetchone()

		if row:
			form = SeasonForm(request.form)
			form.name.default=row['name']
			form.location.default=row['location']
			form.start.default=row['start']
			form.end.default=row['end']
			form.light_hours.default=row['light_hours']
			form.process()
		else:
			return 'Error loading #{id}'.format(id=id)
		title_verb = "Edit"

		return render_template('operation_form.html', formpage='add_season.html', title_verb=title_verb, icon=icon, form=form, row=row,operation=operation,is_login=session.get('logged_in'))
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/season/delete/<int:id>')
def delete_season(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM season WHERE id=%s", (id,))
		conn.commit()
		flash('Season deleted successfully!','info')
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	return redirect("/seasons")
