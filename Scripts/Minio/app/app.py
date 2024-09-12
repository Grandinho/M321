from minio import Minio
from flask import Flask

host = "192.168.100.15:2016"
bucket = "theship-permastore"
access_key = "theship"
secret_key = "theship1234"

minio_client = Minio (
    host,
    access_key=access_key,
    secret_key=secret_key,
    secure=False
)



from flask import Flask

app = Flask(__name__)

@app.route('/<station>/receive')
def receive():
    if not minio_client.bucket_exists("theship-permastore"):
        minio_client.make_bucket('theship-permastore')
    
    return 'Hello world'

@app.route('/<station>/send')
def send():
    if not minio_client.bucket_exists("theship-permastore"):
        minio_client.make_bucket('theship-permastore')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


from minio import Minio
from flask import Flask, request, jsonify
import json
import io
import requests
import base64


app = Flask(__name__)

@app.route('/<station>/receive', methods=['POST'])
def receive(station):
    response = requests.post('http://192.168.100.15:2029/receive')
    payload = json.loads(response.content)
    
    # Extract the Base64 encoded message
    encoded_msg = payload['received_messages'][0]['msg']
    dest = payload['received_messages'][0]['dest']
    # Decode the Base64 message
    byte_array = bytearray(base64.b64decode(encoded_msg))
    # Construct the response in the desired format
    byte_list = list(byte_array)
    
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

def bytes_to_base64(byte_list):
    # Convert the list of integers to bytes
    byte_data = bytes(byte_list)
    
    # Encode the bytes to Base64
    base64_string = base64.b64encode(byte_data).decode('utf-8')
    
    return base64_string

@app.route('/<station>/send', methods=['POST'])
def send(station):
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2023)


def receive(station):
    response = requests.post('http://192.168.100.15:2029/receive')
    # print(response.status_code)
    payload = json.loads(response.content)
    # print(payload)
    encoded_msg = payload['received_messages'][0]['msg']
    byte_array = bytearray(base64.b64decode(encoded_msg))

    return jsonify({"kind": "success", "messages": [byte_array]})

def receive(station):
    response = requests.post('http://192.168.100.15:2029/receive')
    payload = json.loads(response.content)
    
    # Extract the Base64 encoded message
    encoded_msg = payload['received_messages'][0]['msg']
    dest = payload['received_messages'][0]['dest']
    # Decode the Base64 message
    decoded_msg = base64.b64decode(encoded_msg)
    byte_array = bytearray(base64.b64decode(encoded_msg))
    # Construct the response in the desired format
    response_data = {
        "kind": "success",
        "messages": [
            {
                "destination": dest,
                "data": byte_array
            }
        ]
    }
    
    return response_data

print(receive('t'))
