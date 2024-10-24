from flask import Flask, request, jsonify
from websockets.sync.client import connect
import json
import requests
import base64
from typing import List, Tuple
import xmlrpc.client


app = Flask(__name__)

@app.route('/<station>/receive', methods=['POST'])
def receive(station):
    print(station)
    match station:
        case "Azura Station":
            payload = receive_from_azura()
        case "Core Station":
            payload = receive_from_core()
        case "Elyse Terminal":
            payload = receive_from_elyse()
        case "Zurro Station":
            payload = receive_from_zurro()
        case "Station 15-A":
            payload = receive_from_15A()
        # dummy
        case "Illume Colony": 
            payload = receive_from_core()

    return payload

def receive_from_15A() -> List[Tuple[str, bytearray]]:
    server = xmlrpc.client.ServerProxy(" http://192.168.100.15:2034/RPC2")
    result = server.receive()
    messages = []
    for msg in result:
        # print(msg[0])
        # list(msg[1])¨
        messages.append({"destination": msg[0],"data": list(bytearray(msg[1].data))})
        
    response_data = {
        "kind": "success",
        "messages": messages
    }
    
    return response_data

def receive_from_azura():
    response = requests.get('http://192.168.100.15:2030/messages_for_other_stations')
    payload = json.loads(response.content)
    
    # Extract the Base64 encoded message
    encoded_msg = payload['received_messages'][0]['base64data']
    dest = payload['received_messages'][0]['dest']
    # Decode the Base64 message
    byte_array = bytearray(base64.b64decode(encoded_msg))
    byte_list = list(byte_array)
    # Construct the response in the desired format
    response_data = {
        "kind": "success",
        "messages": [
            {
                "destination": dest,
                "data": byte_list
            }
        ]
    }
    
    return response_data

def receive_from_core():
    response = requests.post('http://192.168.100.15:2027/receive')
    payload = json.loads(response.content)
    print(payload)
    
    # Extract the Base64 encoded message
    encoded_msg = payload['received_messages'][0]['data']
    dest = payload['received_messages'][0]['target']
    # Decode the Base64 message
    byte_array = bytearray(base64.b64decode(encoded_msg))
    byte_list = list(byte_array)
    # Construct the response in the desired format
    response_data = {
        "kind": "success",
        "messages": [
            {
                "destination": dest,
                "data": byte_list
            }
        ]
    }
    
    return response_data

def receive_from_zurro():
    response = requests.post('http://192.168.100.15:2029/receive')
    payload = json.loads(response.content)
    
    # Extract the Base64 encoded message
    encoded_msg = payload['received_messages'][0]['msg']
    dest = payload['received_messages'][0]['dest']
    # Decode the Base64 message
    byte_array = bytearray(base64.b64decode(encoded_msg))
    byte_list = list(byte_array)
    # Construct the response in the desired format
    response_data = {
        "kind": "success",
        "messages": [
            {
                "destination": dest,
                "data": byte_list
            }
        ]
    }
    
    return response_data

def receive_from_elyse():
    result = None
    with connect("ws://192.168.100.15:2026/api") as ws:
        while True:
            result = ws.recv()
            print("server <- client: " + result)
            if result:
                break
 
    result = json.loads(result)
    # byte_array = bytearray(base64.b64decode(result["msg"]))
    # byte_list = list(byte_array)
    response_data = {
        "kind": "success",
        "messages": [
            {
                "destination": result["destination"],
                "data": result["msg"]
            }
        ]
    }
    return response_data


def bytes_to_base64(byte_list):
    # Convert the list of integers to bytes
    byte_data = bytes(byte_list)
    
    # Encode the bytes to Base64
    base64_string = base64.b64encode(byte_data).decode('utf-8')
    
    return base64_string

@app.route('/<station>/send', methods=['POST'])
def send(station):
    print(station)
    match station:
        case "Azura Station":
            payload = send_to_azura(request.get_json(force=True))
        case "Core Station":
            payload = send_to_core(request.get_json(force=True))
        case "Elyse Terminal":
            payload = send_to_elyse(request.get_json(force=True))
        case "Zurro Station":
            payload = send_to_zurro(request.get_json(force=True))
    return payload

def send_to_azura(request):
    request_data = request
    # Get data from the request
    sender = request_data['source']
    data = request_data['data']
    msg_as_bytes = bytes_to_base64(data)

    # Generate a unique object name for this station's data
    payload = {
        "sending_station": sender,
        "base64data": msg_as_bytes
    }
    response = requests.post('http://192.168.100.15:2030/put_message',json=payload)
    if response.status_code == 200:
        print(response.content)
        return jsonify({"kind": "success"})
    return response.content, 400

def send_to_core(request):
    request_data = request
    # Get data from the request
    sender = request_data['source']
    data = request_data['data']
    msg_as_bytes = bytes_to_base64(data)

    # Generate a unique object name for this station's data
    payload = {
        "source": sender,
        "message": msg_as_bytes
    }
    response = requests.post('http://192.168.100.15:2027/send',json=payload)
    if response.status_code == 200:
        print(response.content)
        return jsonify({"kind": "success"})
    print(payload)
    return response.content, 400

def send_to_elyse(request):
    request_data = request
    # Get data from the request
    sender = request_data['source']
    data = request_data['data']
    msg_as_bytes = bytes_to_base64(data)

    # Generate a unique object name for this station's data
    payload = {
        "sending_station": sender,
        "base64data": msg_as_bytes
    }
    result = None
    with connect("ws://192.168.100.15:2026/api") as ws:
        while True:
            result = ws.send()
            print("client -> server: " + payload)
            if result:
                break
    return jsonify({"kind": "success"})



def send_to_zurro(request):
    request_data = request
    # Get data from the request
    sender = request_data['source']
    data = request_data['data']
    msg_as_bytes = bytes_to_base64(data)

    # Generate a unique object name for this station's data
    payload = {
        "sending_station": sender,
        "base64data": msg_as_bytes
    }
    response = requests.post('http://192.168.100.15:2029/put_message',json=payload)
    return jsonify({"kind": "success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2023)
