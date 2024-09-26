import pika
import json
import time
import datetime
from pathlib import Path
import communication
import thruster

def get_scanner_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.100.15', port=2014))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)
    
    for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
        # print(json.loads(body.decode('utf-8')))
        payload = json.loads(body.decode('utf-8'))
        captain_morris_seen = False
        for item in payload:
            log(item)
            if item['name'] == 'Captain Morris':
                captain_morris_seen = True
                x = item['pos']["x"]
                y = item['pos']["y"]
                print('captain morris seen')
                communication.move_to_cordinates(x,y)
            else:
                print(captain_morris_seen)
                if captain_morris_seen:
                    print('thruster')
                    thruster.set_to_idle()
                    thruster.activate_thruster('bottomLeft',0)
                    thruster.activate_thruster('bottomRight',0)
                    thruster.activate_thruster('front',0)
                    thruster.activate_thruster('frontLeft',0)
                    thruster.activate_thruster('frontRight',0)
                    thruster.activate_thruster('back',100)
           
def log(text):
    file_path = Path("C:/Projects/School/M321/scannerLog.txt")
    # print(text)
    with open(file_path, 'a') as outfile:
        # print(outfile.name + "test")
        outfile.write(str(datetime.datetime.now()) + ": " + str(text) + "\n")

get_scanner_data()