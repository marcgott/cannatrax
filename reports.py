import pymysql
from app import app
from cannatrax import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import *
from matplotlib.dates import DateFormatter
import numpy as np
import seaborn as sns
import base64
import calendar
from datetime import date,datetime
from io import BytesIO
from db_config import mysql
from flask import session, redirect

@app.route('/reports')
def show_reports():
    if not session.get('logged_in'):
        return redirect("/")
    try:
        option = get_settings()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Height Comparison
        sql = "select plant.name, plant.id, MAX(log.height) as height, MAX(log.span) as span from log INNER JOIN plant on plant.id=log.plant_ID group by plant_ID ORDER BY height,span"
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        height_comparison = get_height_comparison(data)
        return render_template("reports.html",height_comparison=height_comparison.decode('utf8'),icon=get_icons(),option=option,is_login=session.get('logged_in'))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# Get current height/span of all plants
sql = "SELECT DISTINCT(plant_ID),max(height) as maxheight ,max(span) as maxspan FROM `log` group by plant_ID"
