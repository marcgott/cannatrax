#! /usr/bin/env python3.5

import pymysql
from app import app
from db_config import mysql
from flask import jsonify, flash, request, session, abort
from pytz import all_timezones
from forms import *
from tables import *
from plants import *
from cycles import *
from strains import *
from environments import *
from nutrients import *
from repellents import *
from log import *

program_name="CannaTrax"

@app.route('/api/login', methods=['POST'])
def do_api_login():
	option = get_settings();

	print("API LOGIN CALLED")
	request.get_json(force=True)
	_json = request.json
	api_key = _json['api_key']
	if _json['api_key'] == app.config['API_KEY']:
		resp = jsonify({"api_authentcation":"success"})
		session['logged_in'] = True
		resp.status_code = 200
		return resp
	else:
		resp = jsonify({"message":"bad_api_key"})
		resp.status_code = 500
		print(resp)
		return resp


@app.route('/api/log', methods=['GET'])
def do_api_get_log():
	option = get_settings();
	print("API LOG CALLED")
	if True:
		try:
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT id,name FROM plant")
			rows = cursor.fetchall()
			#print(rows)
			resp = jsonify({'results':rows})
			resp.status_code = 200
			#print(resp)
			return resp
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			conn.close()

	else:
		resp = jsonify({"message":"get log error"})
		resp.status_code = 500
		print(resp)
		return resp

@app.route('/api/plant/view/<int:id>', methods=['GET'])
def do_api_get_plant_view(id):
	option = get_settings();
	print("API PLANT VIEW ",id," CALLED")
	if True:
		try:
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			#cycle_ID,strain_ID,current_environment
			cursor.execute("SELECT * FROM plant WHERE id=%s",(id))
			row = cursor.fetchone()
			#print(rows)
			resp = jsonify({'results':row})
			resp.status_code = 200
			return resp
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			conn.close()

	else:
		resp = jsonify({"message":"get log error"})
		resp.status_code = 500
		print(resp)
		return resp
