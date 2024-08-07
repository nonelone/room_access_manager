import requests
import config

host = input("$ host IP (without /api) > ")
while True:
    token = input("$ token > ")
    key = input("$ key card > ")
    try:
        with requests.post(host, data={'token' : token, 'card_id' : key}) as r:
            print(r.status_code, r.reason)
            print(r.text)

    except: break
