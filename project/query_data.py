import pandas as pd
import datetime
from influxdb_client import InfluxDBClient
import numpy as np

def query_data():
    my_token = "8aXPa1s0mNMDXexrRDbG5WKd6flwalEg-PnTHhsM-xcPWuEFApJqo1CMrwfjzWNVB_BMZqAHQvBlRKuFJpnhRg=="
    my_org = "anais@influxdata.com"
    bucket = "my-bucket"
    query= '''
    from(bucket: "my-bucket")
    |> range(start:-40d, stop: now())
    |> filter(fn: (r) => r._measurement == "cpu")
    |> filter(fn: (r) => r._field == "usage_user")
    |> filter(fn: (r) => r.cpu == "cpu-total")
    |> top(n:10)'''

    url = "https://us-west-2-1.aws.cloud2.influxdata.com/"

    client = InfluxDBClient(url=url, token=my_token, org=my_org, debug=False)
    df = client.query_api().query_data_frame(org=my_org, query=query)
    value = df["_value"].to_numpy()
    index = [datetime.to_pydatetime() for datetime in df["_time"]]
    ts = pd.Series(value, index=index)

    # ts = pd.Series(system_stats["_value"], index=system_stats["_time"])
    
    # print(ts)
    return ts