import requests
import json
import os
import secrets

BOLD = '\u001b[1m'
WHITE  = '\33[37m'
END = '\033[0m'

flask_token = "8aXPa1s0mNMDXexrRDbG5WKd6flwalEg-PnTHhsM-xcPWuEFApJqo1CMrwfjzWNVB_BMZqAHQvBlRKuFJpnhRg=="
flask_orgid = "0437f6d51b579000"
print(flask_token)
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
    print(json.dumps(pretty_json, indent=2))

    authID = pretty_json["id"]
    token =  pretty_json["token"]
    print("Your new token:\n ", token)
    print(WHITE + BOLD + "Keep it secret! Keep it safe!" + END + END)
    return token