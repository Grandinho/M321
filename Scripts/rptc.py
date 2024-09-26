import xmlrpc.client
from typing import List, Tuple
import base64
import json

# Verbindung zum XML-RPC-Server herstellen mit dem angegebenen Endpoint
server = xmlrpc.client.ServerProxy("http://192.168.100.15:2024/RPC2")

def send_message(source: str, data: bytes) -> str:
    result = server.send(source, xmlrpc.client.Binary(data))
    return result

def receive_messages() -> List[Tuple[str, bytearray]]:
    result = server.receive()
    for msg in result:
        # print(msg[0])
        # list(msg[1])
        print(list(bytearray(msg[1].data)))
        # print(data['data'])
    # return [(msg[0], to_byte_array(msg[1].data)) for msg in result]

def bytes_to_base64(byte_list):
    # Convert the list of integers to bytes
    byte_data = bytes(byte_list)
    
    # Encode the bytes to Base64
    base64_string = base64.b64encode(byte_data).decode('utf-8')
    
    return base64_string

def to_byte_array(msg):
    print(msg)
    byte_array = bytearray(base64.b64decode(msg))
    return list(byte_array)

# Beispielverwendung
# if __name__ == "__main__":
#     source = "TestClient"
#     data = b"Hallo Artemis Station!"

    # try:
    #     # Senden
    #     send_result = send_message(source, data)
    #     print(f"Sende-Ergebnis: {send_result}")

    #     # Empfangen
    #     received_messages = receive_messages()
    #     for destination, message_data in received_messages:
    #         print(f"Empfangen von {destination}: {message_data.decode('utf-8', errors='replace')}")

    # except xmlrpc.client.Fault as err:
    #     print(f"Ein Fehler ist aufgetreten: {err}")
    # except ConnectionError:
    #     print("Verbindungsfehler: Konnte keine Verbindung zum Server herstellen.")
    # except Exception as e:
    #     print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

receive_messages()
# print(received_messages)