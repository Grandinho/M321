import requests

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
    if response.content == "TODO: when to fast":
        switch(x,y,x1,y1)

def move_to_bottom():
    for x in range(11):
        for y in range(8):
            # data = {
            # "a": {"x": x, "y": y}, 
            # "b": {"x": x, "y": y+1}
            # }
            switch_local(x,y,x,y+1)

print(inventory[0][0])

move_to_bottom()
for x in range(9):
    print(inventory[x])
        

