import requests
import config

host = input("$ host IP (with protocol & without /api) > ")
while True:
    token = input("$ token > ")
    key = input("$ key card > ")
    try:
        print("Checking...")
        with requests.post(host, data={'token' : token, 'card_id' : key}) as r:
            print(r.status_code, r.reason)
            print(r.text)

    except: break