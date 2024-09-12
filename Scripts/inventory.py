import requests
import json

inventory = [['i','i','i','i','i','i','i','i','i','i','i'],
             ['','','','','','','','','','',''],
             ['','','','','','','','','','',''],
             ['','','','','','','','','','',''],
             ['','','','','','','','','','',''],
             ['','','','','','','','','','',''],
             ['','','','','','','','','','',''],
             ['','','','','','','','','','',''],
             ['','','','','','','','','','','']]

def switch_local(x,y,x1,y1):
    inventoryTemp = inventory[y][x]
    inventory[y][x] = inventory[y1][x1]
    inventory[y1][x1] = inventoryTemp

def switch(x,y,x1,y1):
    data = {
        "a": {"x": x, "y": y}, 
        "b": {"x": x1, "y": y1}}
    response = requests.post('http://192.168.100.15:2012/swap_adjacent', json=data)
    print(response.content)
    message = extract_message(response.content)
    if message == "robot is already active. Please wait":
        switch(x,y,x1,y1)

def move_to_bottom():
    for x in range(12):
        for y in range(10):
            inventory = get_inventory()
            if str(inventory[y][x]) != 'None':
                print(inventory[y][x])
                switch(x,y,x,y+1)

def extract_message(response_string):
    try:
        data = json.loads(response_string)
        return data.get('message', 'No message provided')
    except json.JSONDecodeError:
        return 'Invalid JSON response'

def get_inventory():
    response = requests.get('http://192.168.100.15:2012/structure')
    structure = json.loads(response.content)
    return structure["hold"]

while True:
    move_to_bottom()