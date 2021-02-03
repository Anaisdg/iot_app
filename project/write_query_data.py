import pandas as pd
from datetime import datetime
from influxdb_client import InfluxDBClient
import numpy as np
from flask_login import current_user
from flask_login import login_user, logout_user, login_required

def query_data():
    my_token = current_user.read_token
    my_user = current_user.name
    my_org = "anais@influxdata.com"
    bucket = "my-bucket"
    query= '''
    from(bucket: "my-bucket")
    |> range(start:-30d, stop: now())
    |> filter(fn: (r) => r._measurement == "''' + my_user + '''")
    |> filter(fn: (r) => r["_field"] == "value")
    |> tail(n:10)'''
    url = "https://us-west-2-1.aws.cloud2.influxdata.com/"
    client = InfluxDBClient(url=url, token=my_token, org=my_org, debug=False)
    df = client.query_api().query_data_frame(org=my_org, query=query)
    if df.empty: 
        rng = pd.date_range('1/1/2011', periods=10, freq='H')
        ts = pd.Series(np.random.randn(len(rng)), index=rng)
    else: 
        value = df["_value"].to_numpy()
        index = [datetime.to_pydatetime() for datetime in df["_time"]]
        ts = pd.Series(value, index=index)    
    return print(ts)

def write_data():
    my_token = current_user.write_token
    my_user = current_user.name
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
    write_api.write(bucket, record=df, data_frame_measurement_name=my_user)
    return print("points written")
 
if __name__ == "__main__":
    query_data()