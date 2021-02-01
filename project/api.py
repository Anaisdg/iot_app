#  api.py

import requests
import json
import os
import secrets

BOLD = '\u001b[1m'
WHITE  = '\33[37m'
END = '\033[0m'

flask_token = os.environ['INFLUX_FLASK_TOKEN'])
flask_orgid = os.environ['INFLUX_FLAS_ORGID'])
proto="http://"
domain="us-west-2-1.aws.cloud2.influxdata.com"
api_path="/api/v2/authorizations/"
url = proto + domain + api_path

def read_token():
    headers = {"Authorization": "Token " + flask_token}
    namehex = secrets.token_hex(3)
    payload = {
        "orgID": flask_orgid,
        "description": "flask read/write token-" + namehex,
        "permissions": [
            {
                "action": "read",
                "resource": {
                    "type": "buckets",
                    "orgID": flask_orgid,
                },
            },
        ],
    }

    r = requests.post(url, headers=headers, json=payload)
    pretty_json = json.loads(r.text)
    # print(json.dumps(pretty_json, indent=2))

    authID = pretty_json["id"]
    read_token =  pretty_json["token"]
    # print("Your new read token:\n ", read_token)
    # print(WHITE + BOLD + "Keep it secret! Keep it safe!" + END + END)
    return read_token

def write_token():
    headers = {"Authorization": "Token " + flask_token}
    namehex = secrets.token_hex(3)
    payload = {
        "orgID": flask_orgid,
        "description": "flask read/write token-" + namehex,
        "permissions": [
            {
                "action": "write",
                "resource": {
                    "type": "buckets",
                    "orgID": flask_orgid,
                },
            },
        ],
    }

    r = requests.post(url, headers=headers, json=payload)
    pretty_json = json.loads(r.text)
    # print(json.dumps(pretty_json, indent=2))

    authID = pretty_json["id"]
    write_token =  pretty_json["token"]
    # print("Your new read token:\n ", read_token)
    # print(WHITE + BOLD + "Keep it secret! Keep it safe!" + END + END)
    return write_token