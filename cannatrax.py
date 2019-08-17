import pymysql
from app import app
from db_config import mysql
from flask import session, redirect
from forms import LoginForm

def check_login():
    if not session.get('logged_in'):
        return False
    return True


def get_settings():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM options")
		rows = cursor.fetchall()
		options={}
		for row in rows:
			key = row['option_key']
			value = row['option_value']
			options[key]=value
		return options
	except Exception as e:
		print(e)
