import requests

while True:
    token = input("$ token > ")
    key = input("$ key card > ")
    try:
        with requests.post('http://127.0.0.1:5000/api', data={'token' : token, 'card_id' : key}) as r:
            print(r.status_code, r.reason)
            print(r.text)

    except: break   