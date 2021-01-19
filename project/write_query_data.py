import pandas as pd
from datetime import datetime
from influxdb_client import InfluxDBClient
import numpy as np
from flask_login import current_user
from flask_login import login_user, logout_user, login_required

def query_data():
    # flask_token = "8aXPa1s0mNMDXexrRDbG5WKd6flwalEg-PnTHhsM-xcPWuEFApJqo1CMrwfjzWNVB_BMZqAHQvBlRKuFJpnhRg=="
    # flask_orgid = "0437f6d51b579000"
    # print(current_user)
    my_token = current_user.token
    # my_token = "8aXPa1s0mNMDXexrRDbG5WKd6flwalEg-PnTHhsM-xcPWuEFApJqo1CMrwfjzWNVB_BMZqAHQvBlRKuFJpnhRg=="
    print(my_token)
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
    # print(ts)
    return ts

def write_data():
    my_token = "8aXPa1s0mNMDXexrRDbG5WKd6flwalEg-PnTHhsM-xcPWuEFApJqo1CMrwfjzWNVB_BMZqAHQvBlRKuFJpnhRg=="
    my_org = "anais@influxdata.com"
    bucket = "my-bucket"
    url = "https://us-west-2-1.aws.cloud2.influxdata.com/"
    client = InfluxDBClient(url=url, token=my_token, org=my_org, debug=False)
    df = pd.DataFrame(np.random.randint(0,100,size=(5, 1)), columns=list('value'))
    # datetime object containing current date and time
    now = datetime.now()
    dti = pd.date_range(now, periods=3, freq="M")
    df = df.set_index(dti)
    write_client.write(bucket, record=df, data_frame_measurement_name=current_user.name)
    
    return print("points written")
 
if __name__ == "__main__":
    query_data()