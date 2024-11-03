from concurrent import futures
import grpc
import api_pb2
import api_pb2_grpc
from shield_generator import ShieldGeneratorDB

class SensorVoidEnergyServer(api_pb2_grpc.SensorVoidEnergyServerServicer):
    def read_sensor_data(self, request, context):
        shieldgenerator = ShieldGeneratorDB()
        shieldgenerator.connect()
        sensor_data = shieldgenerator.get_vacuum_energy_data()
        return api_pb2.SensorData(hexdata=sensor_data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_SensorVoidEnergyServerServicer_to_server(
        SensorVoidEnergyServer(), server
    )
    server.add_insecure_port('[::]:2102')
    server.start()
    # server.add_insecure_port
    print("Server gestartet auf 192.168.100.15:2102")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()