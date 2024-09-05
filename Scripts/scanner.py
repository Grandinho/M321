import pika
import json
import time
import datetime
from pathlib import Path

def get_scanner_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.100.15', port=2014))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)
    
    for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
        print(json.loads(body.decode('utf-8')))
        payload = json.loads(body.decode('utf-8'))
        print(payload)
        for item in payload:
            log(item)
            # if item['name'] == 'Station 15-A':
            #     x = item['pos']["x"]
            #     y = item['pos']["y"]
           
def log(text):
    file_path = Path("C:/Projects/School/M321/scannerLog.txt")
    print(text)
    with open(file_path, 'a') as outfile:
        print(outfile.name + "test")
        outfile.write(str(datetime.datetime.now()) + ": " + str(text) + "\n")

get_scanner_data()