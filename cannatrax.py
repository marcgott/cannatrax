import pymysql
from app import app
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import *
from matplotlib.dates import DateFormatter
import numpy as np
import seaborn as sns
import base64
import calendar
import requests
from datetime import date,datetime
from io import BytesIO
from db_config import mysql
from flask import session, redirect, render_template

#sns.set_style("whitegrid")

def check_login():
    if not session.get('logged_in'):
        return False
    return True

def get_icons(operation=None):
    icons = {'dashboard':'tachometer-alt','log':'clipboard-check','plants':'leaf','environments':'spa','nutrients':'tint','repellents':'bug','strains':'dna','cycles':'sun','reports':'file-contract','settings':'bars','germination':'egg','seedling':'seedling','vegetation':'leaf','pre-flowering':'spa','flowering':'cannabis','harvest':'tractor','archive':'eye-slash','dead':'skull-crossbones','gender':'venus-mars','source':'shipping-fast'}
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

def get_daystats(dt=None):
    option=get_settings()

    daydate = date.today()
    print(daydate)
    req = 'https://api.sunrise-sunset.org/json?lat=%s&lng=%s&date=%s' % (option['latitude'],option['longitude'],daydate)
    res = requests.get(req)
    #print(res.json)
    return res.text

def get_measurement_plot(rows,plant_name):
    option=get_settings()

    labels = []
    heights= []
    spans = []
    trims = []
    last_span = 0
    last_height = 0
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


    for i,trim in enumerate(trims):
        if trim['type'] != '':
            color = "".join(['C',str(i)])
            plt.axvline(trim['date'],label=trim['type'],color=color)

    labels.append(date.today())
    ax.set_ylabel(option['length_units'])
    ax.set_xlim([min(labels),max(labels)])
    ax.set_xticks(labels)
    ax.set_xticklabels(labels)
    ax.grid(True, linestyle='-')
    ax.tick_params( width=3, grid_color='g', grid_alpha=0.5)
    ax.set_ylim([0,ylimit])
    ax.set_title('Growth Chart for '+plant_name)
    formatter = DateFormatter('%m/%d/%y')
    for tick in ax.xaxis.get_majorticklabels():
        tick.set_horizontalalignment("right")
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    ax.legend()
    fig.tight_layout()

    figfile = BytesIO()
    fig.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file

    #figdata_png = base64.b64encode(figfile.read())
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png

def get_water_calendar(dates,plant_name):
    sns.set_style("whitegrid")
    plt.figure(figsize=(9, 3))
    # non days are grayed
    ax = plt.gca().axes
    ax.add_patch(Rectangle((29, 2), width=.8, height=.8,
                           color='gray', alpha=.3))
    ax.add_patch(Rectangle((30, 2), width=.8, height=.8,
                           color='gray', alpha=.5))
    ax.add_patch(Rectangle((31, 2), width=.8, height=.8,
                           color='gray', alpha=.5))
    ax.add_patch(Rectangle((31, 4), width=.8, height=.8,
                           color='gray', alpha=.5))
    ax.add_patch(Rectangle((31, 6), width=.8, height=.8,
                           color='gray', alpha=.5))
    ax.add_patch(Rectangle((31, 9), width=.8, height=.8,
                           color='gray', alpha=.5))
    ax.add_patch(Rectangle((31, 11), width=.8, height=.8,
                           color='gray', alpha=.5))

    waterdays = []
    watermonths = []
    for dt in dates:
        waterdays.append(dt['d'])
        watermonths.append(dt['m'])
    for d, m in zip(waterdays,watermonths):
        ax.add_patch(Rectangle((d, m),
                               width=.8, height=.8, color='C0'))
    plt.yticks(np.arange(1, 13)+.5, list(calendar.month_abbr)[1:])
    plt.xticks(np.arange(1,32)+.5, np.arange(1,32))
    plt.xlim(1, 32)
    plt.ylim(1, 13)
    ax.set_title('Water Chart for '+plant_name)
    plt.gca().invert_yaxis()
    # remove borders and ticks
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.tick_params(top=False, bottom=False, left=False, right=False)
    #plt.show()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file

    #figdata_png = base64.b64encode(figfile.read())
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png

def get_comparison_chart(data,chartname,yaxis_label):
    option=get_settings()
    labels = []
    measures= []

    for row in data:
        labels.append(row['name'])
        measures.append(float(row['measure']))

    fig, ax = plt.subplots()
    ylimit = max(measures) + 5

    d1 = ax.bar(labels,measures,label=chartname)
    plt.axhline(np.average(measures),label="Average",color="r")

    ax.set_ylabel(yaxis_label)
    ax.set_xticks(labels)
    ax.set_xticklabels(labels)
    ax.tick_params(width=3)
    ax.set_ylim([0,ylimit])
    ax.set_title('Average Plant '+chartname)
    for tick in ax.xaxis.get_majorticklabels():
        tick.set_horizontalalignment("right")

    ax.xaxis.set_tick_params(rotation=30, labelsize=8)
    ax.legend(loc='upper left')

    plt.tight_layout()
    figfile = BytesIO()
    fig.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file

    #figdata_png = base64.b64encode(figfile.read())
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png
