import communication


import pika
import json
 
communication.move_to_cordinates(-8346,-17215)
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.100.15', port=2014))
# channel = connection.channel()
 
# channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')
# result = channel.queue_declare(queue='', exclusive=True)
# queue_name = result.method.queue
# channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)
 
# for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
#     print(json.loads(body.decode('utf-8')))
#     payload = json.loads(body.decode('utf-8'))
#     print(payload)
#     for item in payload:
#         if item['name'] == 'Station 15-A':
#             x = item['pos']["x"]
#             y = item['pos']["y"]
#             communication.move_to_cordinates(x,y)