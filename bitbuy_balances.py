#!/usr/bin/env python3
import hmac
import hashlib
import requests
import base64
import time
from influxdb import InfluxDBClient
import time

### Just a file in the local dir that contains
# Pub = ""
# Priv = ""
import secrets


client = InfluxDBClient(
    host="localhost",
    port=8086,
    username=secrets.influx_UserName,
    password=secrets.influx_pass,
    database=secrets.influx_db,
    ssl=False,
)


def send_to_influx(json_data):
    # client.switch_database("crypto")
    return client.write_points(json_data)


stamp = int(round(time.time() * 1000))

## this could done way better, at least in a more modular way. It took a while
# to realise the {} where included in the hmac_msg.

## I also havent figured out content-length

# api_address = f"https://partner.bcm.exchange/api/v1/coins?apikey={Pub}&stamp={stamp}"
# json_data = f'{{\"path\":\"/api/v1/coins\",\"content-length\":-1,\"query\":\"apikey={Pub}&stamp={stamp}\"}}'

api_address = (
    f"https://partner.bcm.exchange/api/v1/wallets?apikey={secrets.Pub}&stamp={stamp}"
)
json_data = f'{{"path":"/api/v1/wallets","content-length":-1,"query":"apikey={secrets.Pub}&stamp={stamp}"}}'


# https://docs.python.org/3/library/stdtypes.html?highlight=bytes#bytes
hmac_msg = bytes(json_data, "UTF-8")
hmac_key = bytes(secrets.Priv, "UTF-8")
# https://docs.python.org/3/library/hmac.html?highlight=hmac#module-hmac
hmac_val = hmac.new(key=hmac_key, msg=hmac_msg, digestmod=hashlib.sha256).digest()
# https://docs.python.org/3/library/base64.html?highlight=base64#module-base64
sig = base64.b64encode(hmac_val).decode()

print(f"Hmac_key: {hmac_key}")
print(f"hmac_msg: {hmac_msg}")
print(f"Hmac_val: {hmac_val}")
print(f"Base64Sig: {sig}\n\n")

headers = {"Content-Type": "application/json", "signature": sig}
response = requests.request("GET", api_address, headers=headers)
response.json()
response.status_code

## Needs to be in ns for influxdb
timestamp = time.time_ns()
json_body = []
fiat_sum = 0

for wallet in response.json():
    if wallet["balance"] != 0:
        json_body.append(
            {
                "measurement": wallet["symbol"],
                "time": timestamp,
                "fields": {
                    "balance": wallet["balance"],
                    "availableBalance": wallet["availableBalance"],
                    "reservedBalance": wallet["reservedBalance"],
                    "fiatCurrencySymbol": wallet["fiatCurrencySymbol"],
                    "fiatBalance": wallet["fiatBalance"],
                },
            }
        )
        fiat_sum += wallet["fiatBalance"]

json_body.append(
    {
        "measurement": "fiat_sum",
        "time": timestamp,
        "fields": {
            "total_cad": fiat_sum,
        },
    }
)
send_to_influx(json_body)
