import inventory
import requests
import json
import asyncio
import time
 
items = 0
def farm_money_with_silver():
    move_to_station("Vesta Station")
    while(is_station_in_reach('Vesta Station') == False):
        is_station_in_reach('Vesta Station')
    free_size = get_free_storage()
    print(free_size)
    if free_size <= 11:
        buy_ressource("Vesta Station", "IRON", free_size)
        inventory.move_to_bottom()
    else:
        steps = int(free_size / 10)
        for x in range(steps):
            buy_ressource("Vesta Station", "IRON", 10)
            inventory.move_to_bottom()
    
    move_to_station("Core Station")
    while(is_station_in_reach("Core Station") == False):
        is_station_in_reach("Core Station")
    iron_amt = get_ressource_amount('IRON')
    sell_items("Core Station", "IRON", iron_amt)

def farm_money_with_gold():
    move_to_cordinates(4296,-5278)
    
   
 
def sell_items(station, what, amount):
    sell_url = "http://192.168.100.15:2011/sell"
    sell_data = {
    "station": station,
    "what": what,
    "amount": amount
    }
   
    json_data = json.dumps(sell_data)
    response = requests.post(sell_url, json_data)
 
    print(response.json())
   
def buy_ressource(station, what, amount):
    buy_url = "http://192.168.100.15:2011/buy"  
    buy_data = {
    "station": station,
    "what": what,
    "amount": amount
    }
   
    json_data = json.dumps(buy_data)
    response = requests.post(buy_url, json_data)
 
    print(response.json())
   
def move_to_station(station):
    move_url = "http://192.168.100.15:2009/set_target"
    station_data = {
        "target": station
    }
   
    json_data = json.dumps(station_data)
    response = requests.post(move_url, json_data)
   
    print(response.json())

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

def move_to_architect_colony():
    move_url = "http://192.168.100.15:2009/set_target"
    station_data = {
        "target": {
            "x": -48911,
            "y": -49878
        }
    }
   
    json_data = json.dumps(station_data)
    response = requests.post(move_url, json_data)
   
    print(response.json())
   
def get_free_storage():
    storage_url = "http://192.168.100.15:2012/hold"
    print('test')
    response = requests.get(storage_url)
 
    # Parse the JSON response
    print(response.content)
    response_data = json.loads(response.content)
    print(response_data)
 
    # Extract the 'hold_size' from the 'hold' object in the response
    hold_size = response_data['hold']['hold_size']
    hold_free = response_data['hold']['hold_free']
    return hold_free

def get_ressource_amount(ressource):
    storage_url = "http://192.168.100.15:2012/hold"
   
    response = requests.get(storage_url)
 
    # Parse the JSON response
    print(response.content)
    response_data = json.loads(response.content)
    print(response_data)
 
    # Extract the 'hold_size' from the 'hold' object in the response
    if ressource in response_data['hold']['resources']:
        return response_data['hold']['resources'][ressource]
    else:
        return 0

def is_station_in_reach(station_name):
    url = "http://192.168.100.15:2011/stations_in_reach"
    response = requests.get(url)
    payload = json.loads(response.content)
    print(response.content)
    if "stations" in payload:
        stations = payload["stations"]
        if station_name in stations:
            return True
        else:
            return False
   