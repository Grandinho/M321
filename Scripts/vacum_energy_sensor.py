import requests
import json

class vacum_energy_sensor:
    def __init__(self, request_id):
        self.endpoint = 'http://192.168.100.15:2037'
        self.request_id = request_id

    def triger_measurement(self): 
        data = {"request_id": self.request_id}
        response = requests.post(f'{self.endpoint}/trigger_measurement',json=data)
        if response.status_code == 201:
            print(response.content)
        else:
            print(response.content)
    
    def get_state(self):
        response = requests.get(f'{self.endpoint}/measurements/{self.request_id}')
        if response.status_code == 200:
            payload = json.loads(response.content)
            print(payload)
            if "result" in payload:
                return payload["result"] 
            else: 
                return ""
        else:
            print(f"error: {response.content}")

    def delete_request(self):
        response = requests.delete(f'{self.endpoint}/measurements/{self.request_id}')
        if response.status_code == 201:
            print(response.content)
        else:
            print(response.content)

v = vacum_energy_sensor("my_id_test")
# v.triger_measurement()
# print(v.get_state())
# print(v.get_state())
    