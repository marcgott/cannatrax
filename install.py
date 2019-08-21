#! /usr/bin/env python3.5

import pymysql
from app import app
from flask import flash, jsonify,render_template, request, redirect,session, abort
from forms import *
from tables import *

@app.route('/install')
def do_install():
    dbcredform = InstallForm(request.form)
    settingsform = SettingsForm(request.form)
    return render_template('install.html', is_install=True, settingsform=settingsform, dbcredform=dbcredform,program_name=app.program_name)

@app.route('/install/check_db', methods=['POST'])
def do_install_checkdb():
    try:
        dbcred = request.form
        connection = pymysql.connect(host=dbcred['dbhost'],user=dbcred['dbuname'],password=dbcred['dbpass'],db=dbcred['dbname'],cursorclass=pymysql.cursors.DictCursor)
        return jsonify({"success":connection.db.decode('utf-8')})
    except pymysql.err.OperationalError as e:
        return jsonify(e.args[0])

@app.route('/install/settings', methods=['POST'])
def do_install_settings():
    try:
        settings = request.form
        connection = pymysql.connect(host=settings['dbhost'],user=settings['dbuname'],password=settings['dbpass'],db=settings['dbname'],cursorclass=pymysql.cursors.DictCursor)
        #install sql
        #INSERT INTO settings()
        #with(open db_config.py)
        return jsonify({"success":connection.db.decode('utf-8')})
    except pymysql.err.OperationalError as e:
        return jsonify(e.args[0])
