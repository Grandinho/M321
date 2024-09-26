
import asyncio
import requests
import aiohttp
import keyboard
 
thrusters = {
    "back": "http://192.168.100.15:2003/thruster",
    "bottomLeft": "http://192.168.100.15:2007/thruster",
    "bottomRight": "http://192.168.100.15:2008/thruster",
    "front": "http://192.168.100.15:2004/thruster",
    "frontLeft": "http://192.168.100.15:2005/thruster",
    "frontRight": "http://192.168.100.15:2006/thruster"
}
 
thruster_states = {key: 0 for key in thrusters}
 
def set_to_idle():
    data = {"target": "idle"}
    response = requests.post('http://192.168.100.15:2009/set_target',json=data)
    print(response.content)


def activate_thruster(thruster_name, thrust_percent):
    url = thrusters.get(thruster_name)
    if url:
        data = {"thrust_percent": thrust_percent}
        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                thruster_states[thruster_name] = thrust_percent
            else:
                print(f"Failed to update {thruster_name} (Status: {response.status_code})")
        except Exception as e:
            print(f"Error while updating {thruster_name}: {e}")

async def control_thrusters():
    async with aiohttp.ClientSession() as session:
        keys = {
            "A": ["bottomLeft", "frontRight"],
            "D": ["bottomRight", "frontLeft"],
            "W": ["back"],
            "S": ["front"],
            "Q": ["frontLeft", "bottomLeft"],
            "E": ["frontRight", "bottomRight"]
        }
        while True:
            tasks = []
            active_thrusters = set()
 
            for key, thruster_list in keys.items():
                if keyboard.is_pressed(key):
                    active_thrusters.update(thruster_list)
           
            for thruster in thrusters:
                if thruster in active_thrusters:
                    if thruster_states[thruster] != 100:
                        tasks.append(activate_thruster(session, thruster, 100))
                else:
                    if thruster_states[thruster] != 0:
                        tasks.append(activate_thruster(session, thruster, 0))
 
            if tasks:
                await asyncio.gather(*tasks)
 
            await asyncio.sleep(0.1)
 
if __name__ == "__main__":
    print("Drücke W, A, S, D, Q oder E, um das Raumschiff zu steuern. ESC zum Beenden.")
    try:
        asyncio.run(control_thrusters())
    except KeyboardInterrupt:
        print("Beenden...")