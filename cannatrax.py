import pymysql
from app import app
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import base64
from io import BytesIO
from db_config import mysql
from flask import session, redirect
from forms import LoginForm

#matplotlib.style.use("seaborn-whitegrid")
sns.set_style("whitegrid")

def check_login():
    if not session.get('logged_in'):
        return False
    return True

def get_icons(operation=None):
    icons = {'dashboard':'tachometer-alt','log':'clipboard-check','plants':'leaf','environments':'spa','nutrients':'tint','repellents':'bug','strains':'dna','seasons':'sun','reports':'file-contract','settings':'bars','germination':'egg','seedling':'seedling','vegitation':'leaf','pre-flowering':'spa','flowering':'cannabis','harvest':'tractor','archive':'eye-slash','dead':'skull-crossbones','gender':'venus-mars','source':'shipping-fast'}
    return icons
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

def get_measurement_plot(rows,plant_name):
    option=get_settings()

    labels = []
    heights= []
    spans = []
    trims = []
    last_span = None
    last_height = None
    print(rows)
    for row in rows:
        labels.append(row['logdate'])
        if row['height'] >0:
            heights.append(row['height'])
            last_height = row['height']
        else:
            heights.append(last_height)

        if row['span'] >0:
            spans.append(row['span'])
            last_span = row['span']
        else:
            spans.append(last_span)
        #spans.append(row['span'])
        trims.append({'date':row['logdate'],'type':row['trim']})

    x = np.arange(len(labels))  # the label locations
    fig, ax = plt.subplots()

    ylimit = int(max(heights + spans) + 10)
    d1 = ax.plot_date(labels,heights,fmt='o', tz=None, xdate=True, ydate=False,linestyle='-',label="Height" )
    d2 = ax.plot_date(labels,spans,fmt='o', tz=None, xdate=True, ydate=False,linestyle='-',label="Span")


    trim_color = {'Topping':'#993333','Lollipop':'#339933','Fimming':'#333399','ICE':'#666666'}

    for trim in trims:
        if trim['type'] != '':
            print(trim_color[trim['type']])
            plt.axvline(trim['date'],label=trim['type'],color=trim_color[trim['type']])

    ax.set_ylabel(option['length_units'])
    ax.set_xlim([min(labels),max(labels)])
    ax.set_ylim([0,ylimit])
    ax.set_title('Growth Chart for '+plant_name)

    ax.legend()
    fig.tight_layout()

    figfile = BytesIO()
    fig.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file

    #figdata_png = base64.b64encode(figfile.read())
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png
