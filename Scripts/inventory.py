import requests
import json
import time

def switch(x,y,x1,y1):
    data = {
        "a": {"x": x, "y": y}, 
        "b": {"x": x1, "y": y1}}
    print(data)
    response = requests.post('http://192.168.100.15:2012/swap_adjacent', json=data)
    # print(response.content)
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

def is_column_sorted(col):
    inventory = get_inventory()
    rows = len(inventory)
    has_empty_place = False
    for y in range(rows-1,-1,-1):
        if str(inventory[y][col]) == 'None':
            has_empty_place = True
        else:  
            if has_empty_place:
                return False
    return True

inventory = get_inventory()
rows = len(inventory)
columns = len(inventory[0])
steps = 0
x = 0
# switch(10,3,10,4)

while x < columns:
    while(not is_column_sorted(x)):
        y = rows - 1
        while y >= 0 and y<rows:
                    # print(str(inventory[y][x]))
                    if str(inventory[y][x]) == 'None':
                        # print('None')
                        steps += 1
                        y -= 1
                    else:  
                        if steps > 0:
                            # print("y before: " + str(y))
                            # print("inventory before:" + str(inventory[3][10]))
                            # print("inventory before:" + str(inventory[4][10]))
                            for step in range(1,steps+1,1):
                                switch(x,y+step-1,x,y+step)
                                print('')
                            # print("steps: " + str(steps))
                            y = rows-1
                            # print("y after: " + str(y))
                            steps = 0
                            time.sleep(1)
                            inventory = get_inventory()
                            
                            # print("inventory after:" + str(inventory[3][10]))
                            # print("inventory after:" + str(inventory[4][10]))
                            # print(inventory[y][x])
                        else:
                            y -= 1
                    # print(y)
    x = x+1
