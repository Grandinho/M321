import requests
import json
import time

IP_ADRESS = 'http://192.168.100.15:2012'
ROWS = 11
COLUMNS = 12

def switch(x,y,x1,y1):
    # time.sleep(3)
    data = {
        "a": {"x": x, "y": y}, 
        "b": {"x": x1, "y": y1}}
    response = requests.post(f'{IP_ADRESS}/swap_adjacent', json=data)
    # print(response.content)
    message = extract_message(response.content)
    if message == "robot is already active. Please wait":
        switch(x,y,x1,y1)

def move_to_bottom():
    for y in range(ROWS):
        for x in range(COLUMNS):
            time.sleep(1)
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
    response = requests.get(f'{IP_ADRESS}/structure')
    structure = json.loads(response.content)
    # print(response.content)
    return structure["hold"]

def get_hold():
    response = requests.get(f'{IP_ADRESS}/hold')
    structure = json.loads(response.content)
    return structure["hold"]

def get_free_storage():
    hold = get_hold()
    hold_free = hold['hold_free']
    return int(hold_free)

def get_hold_size():
    hold = get_hold()
    hold_free = hold['hold_size']
    return int(hold_free)

def set_every_item_apart():
    for y in range(ROWS):
        for x in range(COLUMNS):
            time.sleep(2)
            inventory = get_inventory()
            empty_slot = (x+1 + y+1) % 2 == 0
            print(f'x: {x} y: {y} : {empty_slot}')
            if empty_slot:
                if str(inventory[y][x]) != "None":
                    print(f'item {inventory[y][x]}')
                    print(f'switching [{x}][{y} with [{x+1}][{y}]')
                    switch(x,y,x,y+1)
            else:
                if str(inventory[y][x]) == "None":
                    print(f'item {inventory[y][x]}')
                    print(f'switching [{x}][{y} with [{x+1}][{y}]')
                    switch(x,y,x,y+1)
            print('-----------------------------------------')

# while True:
#     set_every_item_apart()


# items_to_buy = get_free_storage() - (get_hold_size() / 2)
# print(items_to_buy)

while True:
    move_to_bottom()

# switch(0,0,0,1)