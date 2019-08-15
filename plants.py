#! /usr/bin/env python3.5

import pymysql
from app import app
#from flask_table import Table
from db_config import mysql
from flask import flash, render_template, request, redirect
from tables import *

@app.route('/plants')
def plants():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM plant")
		rows = cursor.fetchall()
		table = Plant(rows)
		table.border = True
		return render_template('plants.html', table=table)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/plant/new', methods=['GET','POST'])
def add_new_plant_view():
	try:
		if request.method == 'POST':
			flash('New Plant Added!')
			return redirect('/plant/new')
	except Exception as e:
		print(e)
	try:
		form = PlantForm(request.form)
		return render_template('add_plant.html', form=form)
	except Exception as e:
		print(e)


@app.route('/plant/add', methods=['POST'])
def add_plant():
	try:
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO plant(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User added successfully!')
			return redirect('/')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/plant/edit/<int:id>')
def edit_plant(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM plant WHERE id=%s", id)
		row = cursor.fetchone()
		if row:
			return render_template('edit.html', row=row)
		else:
			return 'Error loading #{id}'.format(id=id)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/plant/update', methods=['POST'])
def update_plant():
	try:
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		_id = request.form['id']
		# validate the received values
		if _name and _email and _password and _id and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			print(_hashed_password)
			# save edits
			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User updated successfully!')
			return redirect('/')
		else:
			return 'Error while updating user'
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
		cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
		conn.commit()
		flash('User deleted successfully!')
		return redirect('/')
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
