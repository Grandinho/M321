from flask import Flask, request, jsonify
import requests
import json


app = Flask(__name__)

def get_data():
    response = requests.get('http://192.168.100.15:2038/data')
    payload = json.loads(response.content)
    if response.status_code != 200:
        print(payload)
        return f"Request error: {response.status_code}"
    return payload["value"]

@app.route('/', methods=['GET'])
def do_GET():    
    data = get_data()

    # Create a JSON response
    response = {
        "data": data,
    }
    
    # Write the response body
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2101)
