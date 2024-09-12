# from minio import Minio
# from flask import Flask

# host = "192.168.100.15:2016"
# bucket = "theship-permastore"
# access_key = "theship"
# secret_key = "theship1234"

# minio_client = Minio (
#     host,
#     access_key=access_key,
#     secret_key=secret_key,
#     secure=False
# )



# from flask import Flask

# app = Flask(__name__)

# @app.route('/<station>/receive')
# def receive():
#     if not minio_client.bucket_exists("theship-permastore"):
#         minio_client.make_bucket('theship-permastore')
    
#     return 'Hello world'

# @app.route('/<station>/send')
# def send():
#     if not minio_client.bucket_exists("theship-permastore"):
#         minio_client.make_bucket('theship-permastore')


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')


from minio import Minio
from flask import Flask, request, jsonify
import json
import io

host = "192.168.100.15:2016"
bucket = "theship-permastore"
access_key = "theship"
secret_key = "theship1234"

minio_client = Minio(
    host,
    access_key=access_key,
    secret_key=secret_key,
    secure=False
)

app = Flask(__name__)

@app.route('/<station>/receive', methods=['POST'])
def receive(station):
    if not minio_client.bucket_exists(bucket):
        minio_client.make_bucket(bucket)
    
    # Generate a unique object name for this station's data
    object_name = station
    
    try:
        # Check if data already exists for this station
        data = minio_client.get_object(bucket, object_name)
        existing_data = json.loads(data.read())
    except:
        existing_data = []

    # Append new data (you may want to implement a more sophisticated data structure)
    # new_data = {"destination": station, "data": existing_data}
    # existing_data.append(new_data)

    # # Convert data to JSON and save it to MinIO
    # json_data = json.dumps(existing_data).encode('utf-8')
    # minio_client.put_object(bucket, object_name, io.BytesIO(json_data), len(json_data))

    return jsonify({"kind": "success", "messages": [existing_data]})

@app.route('/<station>/send', methods=['POST'])
def send(station):
    if not minio_client.bucket_exists(bucket):
        minio_client.make_bucket(bucket)

    # Get data from the request
    request_data = request.json
    
    # Generate a unique object name for this station's data
    object_name = station


    modified_data = {
        "destination": request_data['source'],
        "data": request_data['data']
    }

    # Convert data to JSON and save it to MinIO
    json_data = json.dumps(modified_data).encode('utf-8')
    minio_client.put_object(bucket, object_name, io.BytesIO(json_data), len(json_data))

    return jsonify({"kind": "success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2023)