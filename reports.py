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

        comparison_chart = {}
        # Height Comparison
        sql = "select plant.name, plant.id, MAX(log.height) as measure, MAX(log.span) as span from log INNER JOIN plant on plant.id=log.plant_ID group by plant_ID ORDER BY measure,span"
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        chart = get_comparison_chart(data,"Height",option["length_units"])
        comparison_chart['height_comparison'] = chart.decode('utf8')

        sql = "select plant.name, plant.id, MAX(log.nodes) as measure from log INNER JOIN plant on plant.id=log.plant_ID WHERE log.nodes > 0 GROUP BY plant_ID  ORDER BY measure"
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        chart = get_comparison_chart(data,"Nodes","Number of Nodes")
        comparison_chart['node_comparison'] = chart.decode('utf8')

        sql = "select plant.name, plant.id, COUNT(log.transplant) as measure from log INNER JOIN plant on plant.id=log.plant_ID WHERE log.transplant > 0 GROUP BY plant_ID ORDER BY measure"
        cursor.execute(sql)
        conn.commit()
        data = cursor.fetchall()
        chart = get_comparison_chart(data,"Transplants","Number of Transplants")
        comparison_chart['transplants'] = chart.decode('utf8')

        return render_template("reports.html",comparison_chart=comparison_chart,icon=get_icons(),option=option,is_login=session.get('logged_in'))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# Get current height/span of all plants
sql = "SELECT DISTINCT(plant_ID),max(height) as maxheight ,max(span) as maxspan FROM `log` group by plant_ID"
