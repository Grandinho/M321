from flask import Flask, request, jsonify
from websockets.sync.client import connect
import json
import requests
import base64


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

    return payload

def receive_from_azura():
    response = requests.post('http://192.168.100.15:2030/receive')
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
    match station:
        case "Azura Station":
            payload = send_to_azura(request.json)
        case "Core Station":
            payload = send_to_core(request.json)
        case "Elyse Terminal":
            payload = send_to_elyse(request.json)
        case "Zurro Station":
            payload = send_to_zurro(request.json)
    return payload

def send_to_azura():
    request_data = request.json
    # Get data from the request
    request_data = request.json
    sender = request_data['source']
    data = request_data['data']
    msg_as_bytes = bytes_to_base64(data)

    # Generate a unique object name for this station's data
    payload = {
        "sending_station": sender,
        "base64data": msg_as_bytes
    }
    response = requests.post('http://192.168.100.15:2030/put_message',payload)
    return jsonify({"kind": "success"})

def send_to_core():
    request_data = request.json
    # Get data from the request
    request_data = request.json
    sender = request_data['source']
    data = request_data['data']
    msg_as_bytes = bytes_to_base64(data)

    # Generate a unique object name for this station's data
    payload = {
        "sending_station": sender,
        "base64data": msg_as_bytes
    }
    response = requests.post('http://192.168.100.15:2027/put_message',payload)
    return jsonify({"kind": "success"})

def send_to_elyse():
    request_data = request.json
    # Get data from the request
    request_data = request.json
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



def send_to_zurro():
    request_data = request.json
    # Get data from the request
    request_data = request.json
    sender = request_data['source']
    data = request_data['data']
    msg_as_bytes = bytes_to_base64(data)

    # Generate a unique object name for this station's data
    payload = {
        "sending_station": sender,
        "base64data": msg_as_bytes
    }
    response = requests.post('http://192.168.100.15:2029/put_message',payload)
    return jsonify({"kind": "success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2023)
