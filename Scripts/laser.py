import requests
import json
import time

def activate():
    response = requests.post('http://192.168.100.15:2018/activate')
    payload = json.loads(response.content)
    print(payload)

def is_active():
    response = requests.get('http://192.168.100.15:2018/state')
    payload = json.loads(response.content)
    print(payload)
    return(payload['is_active'])

while True:
    time.sleep(8)
    activate()
    