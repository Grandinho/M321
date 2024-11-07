# import inventory
import json
import requests


def move_to_cordinates(x,y):
    move_url = "http://192.168.100.15:2009/set_target"
    station_data = {
        "target": {
            "x": x,
            "y": y
        }
    }
   
    json_data = json.dumps(station_data)
    response = requests.post(move_url, json_data)
   
    print(response.json())

move_to_cordinates(-37811,44750)
# )

# thruster.set_to_idle()

# while True:
#     inventory.move_to_bottom()
# while True:
#     communication.buy_ressource("Shangris Station","GOLD",12)
#     inventory.move_to_bottom()

# communication.move_to_station("Aurora Station")
# communication.sell_items("Core Station", "GOLD", 71)