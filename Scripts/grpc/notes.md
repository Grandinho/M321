$ echo '{
  "shield_generator": 1.0,
  "sensor_void_energy": 1.0, 
  "analyzer_alpha": 1.0
  }' | curl -T - http://192.168.100.15:2033/limits


docker build -t grand512/grpc-sensor-server:latest .
docker push grand512/grpc-sensor-server:latest
kubectl delete deployment sensor-void-energy-server
kubectl apply -f deployment.yaml