import pandas as pd
from datetime import datetime
from influxdb_client import InfluxDBClient
import numpy as np
from flask_login import current_user
from flask_login import login_user, logout_user, login_required

my_token = "8aXPa1s0mNMDXexrRDbG5WKd6flwalEg-PnTHhsM-xcPWuEFApJqo1CMrwfjzWNVB_BMZqAHQvBlRKuFJpnhRg=="
my_org = "anais@influxdata.com"
bucket = "my-bucket"
query= '''
from(bucket: "my-bucket")
|> range(start:-2d, stop: now())
|> filter(fn: (r) => r._measurement == "three")
|> filter(fn: (r) => r["_field"] == "value")
|> limit(n:10)'''
# print(query)
url = "https://us-west-2-1.aws.cloud2.influxdata.com/"
client = InfluxDBClient(url=url, token=my_token, org=my_org, debug=False)
df = client.query_api().query_data_frame(org=my_org, query=query)
print(df)
value = df["_value"].to_numpy()
index = [datetime.to_pydatetime() for datetime in df["_time"]]
ts = pd.Series(value, index=index)    
print(ts)
