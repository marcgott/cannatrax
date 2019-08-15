#! /usr/bin/env python3.5

import pymysql
from app import app
#from flask_table import Table
from db_config import mysql
from flask import flash, render_template, request, redirect
from wtforms import Form, TextField, SelectField, TextAreaField, validators, StringField, SubmitField
from tables import *
from forms import *

icon="ban-circle"
#
# Show default repellents page, general statistics
@app.route('/repellents')
def show_repellents():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM repellent ORDER BY name ASC")
		rows = cursor.fetchall()
		table = Repellent(rows)
		table.border = True
		total_repellents = len(rows)
		return render_template('repellents.html', table=table, total_repellents=total_repellents,icon=icon)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

#
# Display and process new repellent
@app.route('/repellent/new', methods=['GET','POST'])
def add_new_repellent_view():
	icon=None
	if request.method == 'POST':
		try:
			_name = request.form['name']
			_type = request.form['type']
			_target = request.form['target']
			_notes = request.form['notes']

			sql = "INSERT INTO repellent(name,type,target,notes) VALUES(%s, %s, %s,%s)"
			data = (_name, _type, _target, _notes)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			icon="ban-circle"
			flash('New repellent Added!','info')
		except Exception as e:
			icon="remove"
			flash('New repellent Not Added!','error')
			print(e)

	try:
		form = RepellentForm(request.form)
	except Exception as e:
		print(e)
	title_verb = "Add"
	return render_template('add_repellent.html', title_verb=title_verb, form=form, icon=icon, row=None)

@app.route('/repellent/edit/<int:id>', methods=['POST','GET'])
def edit_repellent(id):
	icon=None
	if request.method == "POST":
		_name = str(request.form['name'])
		_type = request.form['type']
		_target = request.form['target']
		_notes = request.form['notes']
		_id = request.form['id']

		sql = "UPDATE repellent SET name=%s, type=%s, target=%s, notes=%s WHERE id=%s"
		data = (_name, _type, _target, _notes, _id)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql, data)
		conn.commit()
		icon="ban-circle"
		flash('repellent updated successfully!','info')

	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM repellent WHERE id=%s", id)
		row = cursor.fetchone()

		if row:
			form = RepellentForm(request.form)
			form.name.default=row['name']
			form.type.default=row['type']
			form.target.default=row['target']
			form.notes.default=row['notes']
			form.process()
		else:
			return 'Error loading #{id}'.format(id=id)
		title_verb = "Edit"

		return render_template('add_repellent.html', title_verb=title_verb, icon=icon, form=form, row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/repellent/delete/<int:id>')
def delete_repellent(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM repellent WHERE id=%s", (id,))
		conn.commit()
		icon="ban-circle"
		flash('repellent deleted successfully!','info')
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	return redirect('/repellents')
