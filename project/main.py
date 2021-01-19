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
from .write_query_data import query_data as qd


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    # rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    # ts = pd.Series(np.random.randn(len(rng)), index=rng)
    ts = qd()

    graphs = [
        # dict(
        #     data=[
        #         dict(
        #             x=[1, 2, 3],
        #             y=[10, 20, 30],
        #             type='scatter'
        #         ),
        #     ],
        #     layout=dict(
        #         title='first graph'
        #     )
        # ),

        # dict(
        #     data=[
        #         dict(
        #             x=[1, 3, 5],
        #             y=[10, 50, 30],
        #             type='bar'
        #         ),
        #     ],
        #     layout=dict(
        #         title='second graph'
        #     )
        # ),

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
    my_token = "8aXPa1s0mNMDXexrRDbG5WKd6flwalEg-PnTHhsM-xcPWuEFApJqo1CMrwfjzWNVB_BMZqAHQvBlRKuFJpnhRg=="
    my_org = "anais@influxdata.com"
    bucket = "my-bucket"
    url = "https://us-west-2-1.aws.cloud2.influxdata.com/"
    client = InfluxDBClient(url=url, token=my_token, org=my_org, debug=False)
    write_api = client.write_api()
    df = pd.DataFrame(np.random.randint(0,100,size=(5, 1)), columns=['value'])
    # datetime object containing current date and time
    now = datetime.now()
    dti = pd.date_range(now, periods=5, freq="min")
    df = df.set_index(dti)
    print(df)
    write_api.write(bucket, record=df, data_frame_measurement_name=current_user.name)
    print("points written")
    return ("nothing")
 
#background process happening without any refreshing
@main.route('/graph_query_data')
def graph_query_data():
    print(current_user)
    my_token = current_user.token
    # print(my_token)
    my_org = "anais@influxdata.com"
    bucket = "my-bucket"
    query= '''
    from(bucket: "my-bucket")
    |> range(start:-30d, stop: now())
    |> filter(fn: (r) => r._measurement == "three")
    |> filter(fn: (r) => r["_field"] == "value")
    |> tail(n:10)'''
    # print(query)
    url = "https://us-west-2-1.aws.cloud2.influxdata.com/"
    client = InfluxDBClient(url=url, token=my_token, org=my_org, debug=False)
    df = client.query_api().query_data_frame(org=my_org, query=query)
    value = df["_value"].to_numpy()
    index = [datetime.to_pydatetime() for datetime in df["_time"]]
    ts = pd.Series(value, index=index)    
    print("graph_query", ts)
    return ts