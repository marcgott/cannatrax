#! /usr/bin/env python3.5

import pymysql
from app import app
from db_config import mysql
from flask import flash, render_template, request, redirect
from pytz import all_timezones
from tables import *
from plants import *

@app.route('/')
def show_menu():
    return render_template('menu.html')

@app.route('/settings')
def show_settings():
    form = SettingsForm(request.form)
    return render_template('settings.html', form=form)

@app.route('/strains')
def show_strains():
    form = SettingsForm(request.form)
    return render_template('settings.html', form=form)

@app.route('/seasons')
def show_seasons():
    form = SettingsForm(request.form)
    return render_template('settings.html', form=form)

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    #resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()
