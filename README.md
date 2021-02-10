A simple Flask demonstrating the InfluxDB API for IoT apps.

## Setup

To install dependencies:

```
$ cd iot_app
$ virtualenv --python python3 env
$ source env/bin/activate
$ pip install -r requirements.txt
```
## Export env variables
Make sure your token is an all access token. 
```
export INFLUX_FLASK_TOKEN=<my-token>
export INFLUX_FLASK_ORGID=<my-org-id>
```

## Create the sqlite database
```
python 
from project import db, create_app
db.create_all(app=create_app())
```

## Run the App

To run the app:

```
cd iot_app
export FLASK_APP=project
export FLASK_DEBUG=1
flask run
```

## Use the sqlite database: 

Step One:
Create the database if it doesn't already exist.
```
python 
from project import db, create_app
db.create_all(app=create_app())
```

Step Two:
Use the database
```
cd project
sqlite3 db.sqlite
# To list the databases 
.databases
# To view the schema 
.schema
# To query the user table
.mode list 
select * from user;
```
