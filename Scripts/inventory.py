import requests
import json

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

inventory = get_inventory()
rows = len(inventory)
columns = len(inventory[0])
steps = 0

while True:
    for x in range(columns-1):
        step = 0
        for y in range(rows-1,-1,-1):
            if str(inventory[y][x]) == 'None':
                steps += 1
            else:
                # print(inventory[y][0])
                if steps > 0:
                    # print(y)
                    for step in range(1,steps+1,1):
                        switch(x,y+step-1,x,y+step)
                    steps = 0
