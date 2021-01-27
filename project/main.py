# main.py
from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_login import current_user
from influxdb_client import InfluxDBClient
import json
import pandas as pd
import plotly
import numpy as np
from .write_query_data import query_data, write_data


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    ts = query_data()   
    graphs = [
        dict(
            data=[
                dict(
                    x=ts.index,  # Can use the pandas data structures directly
                    y=ts
                )
            ]
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    print(current_user)
    return render_template('profile.html', name=current_user.name, token=current_user.token, ids=ids, graphJSON=graphJSON)

#background process happening without any refreshing
@main.route('/graph_write_data')
def graph_write_data():
    write_data()
    return ("nothing")
 
#background process happening without any refreshing
@main.route('/graph_query_data')
def graph_query_data():
    query_data()
    return ts