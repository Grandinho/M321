from shield_generator import ShieldGeneratorDB
from vacum_energy_sensor import vacum_energy_sensor
import time
import string
import random

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# shieldgenerator = ShieldGeneratorDB()
# shieldgenerator.connect()
# print(shieldgenerator.get_vacuum_energy_data())
while True:
    time.sleep(2)
    id = get_random_string(10)
    print(f"id: {id}")
    v = vacum_energy_sensor(id)
    v.triger_measurement()
    result = ""
    while result == "":
        result = v.get_state()
    print(f"result: {result}")
    shieldgenerator = ShieldGeneratorDB()
    shieldgenerator.connect()
    print(shieldgenerator.get_vacuum_energy_data())
    shieldgenerator.update_vacuum_energy_data(result)
    v.delete_request()
    # v.triger_measurement()
    # v.get_state()s