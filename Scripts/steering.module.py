import asyncio
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
 
async def activate_thruster(session, thruster_name, thrust_percent):
    url = thrusters.get(thruster_name)
    if url:
        data = {"thrust_percent": thrust_percent}
        async with session.put(url, json=data) as response:
            if response.status == 200:
                thruster_states[thruster_name] = thrust_percent
            else:
                print(f"Failed to update {thruster_name} (Status: {response.status})")
 
async def get_angle(session):
    url = "http://192.168.100.15:2010/pos"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            angle = data["pos"]["angle"]
            return angle
        else:
            print(f"Failed to get position (Status: {response.status})")
            return None
 
def calculate_thrust(angle):
    if angle > 180:
        angle -= 360
    return min(max(abs(angle) - 10, 0), 90)
 
async def control_thrusters():
    async with aiohttp.ClientSession() as session:
        keys = {
            "A": ["bottomRight", "frontRight"],
            "D": ["bottomLeft", "frontLeft"],
            "W": ["back"],
            "S": ["front"],
            "Q": ["frontLeft", "bottomLeft"],
            "E": ["frontRight", "bottomRight"]
        }
        await session.post("http://192.168.100.15:2009/set_target", json={"target": "idle"})
        while True:
            tasks = []
            active_thrusters = {}
 
            angle = await get_angle(session)
            if angle:
                thrust = calculate_thrust(angle)
                if 355 >= angle >= 180:
                    active_thrusters["frontLeft"] = thrust
                    active_thrusters["bottomRight"] = thrust
                elif angle >= 5:
                    active_thrusters["frontRight"] = thrust
                    active_thrusters["bottomLeft"] = thrust
 
            for key, thruster_list in keys.items():
                if keyboard.is_pressed(key):
                    for thruster in thruster_list:
                        active_thrusters[thruster] = 100
 
            for thruster in thrusters:
                if thruster not in active_thrusters:
                    active_thrusters[thruster] = 0
 
            for thruster, desired_thrust in active_thrusters.items():
                current_thrust = thruster_states[thruster]
                if current_thrust != desired_thrust:
                    tasks.append(activate_thruster(session, thruster, desired_thrust))
 
            if tasks:
                await asyncio.gather(*tasks)
 
            await asyncio.sleep(0.1)
 
if __name__ == "__main__":
    print("Drücke W, A, S, D, Q oder E, um das Raumschiff zu steuern. ESC zum Beenden.")
    try:
        asyncio.run(control_thrusters())
    except KeyboardInterrupt:
        print("Beenden...")
 