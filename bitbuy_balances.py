#!/usr/bin/env python3
import hmac
import hashlib
import requests
import base64
import time


### Just a file in the local dir that contains
# Pub = ""
# Priv = ""
import secrets


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


for a in response.json():
    if a["balance"] != 0:
        print(a)
