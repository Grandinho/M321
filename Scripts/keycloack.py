import requests

import json


url = "http://192.168.100.15:2018/configure_oauth"

configure_data = {

"client_secret": "Mn0ku4jUnqWEGzKb4iawXS91I3pJ2COF",

"authorize_url": "http://192.168.100.15:8080/realms/laser-login/protocol/openid-connect/auth",

"token_url": "http://192.168.100.15:8080/realms/laser-login/protocol/openid-connect/token"

}


json_data = json.dumps(configure_data)

response = requests.post(url, json_data)


url2 = "http://192.168.100.15:2018/activate"


response2 = requests.post(url2)


print(response.json())

print(response2.json())