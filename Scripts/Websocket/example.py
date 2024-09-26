import json
import base64
from websockets.sync.client import connect
 

def get_elyse_terminal():
    result = None
    with connect("ws://192.168.100.15:2026/api") as ws:
        while True:
            result = ws.recv()
            print("server <- client: " + result)
            if result:
                break
 
    result = json.loads(result)
    byte_array = bytearray(base64.b64decode(result["msg"]))
    byte_list = list(byte_array)
    response_data = {
        "kind": "success",
        "messages": [
            {
                "destination": result["destination"],
                "data": byte_list
            }
        ]
    }
    return response_data