$ echo '{
  "thruster_back": 0.0,
  "thruster_front": 0.0, 
  "sensor_atomic_field": 1.0,
  "matter_stabilizer": 1.0,
  "laser": 0.8,
  "scanner": 0.0,
  "thruster_front_left": 0.0,
  "thruster_front_right": 0.0,
  "thruster_bottom_left": 0.0,
  "thruster_bottom_right": 0.0
  }' | curl -T - http://192.168.100.15:2033/limits

echo '{
  "thruster_back": 1,
  "thruster_front": 1, 
  "sensor_atomic_field": 1.0,
  "matter_stabilizer": 1.0,
  "laser": 0,
  "scanner": 0.0
  }' | curl -T - http://192.168.100.15:2033/limits


docker build -t grand512/grpc-sensor-server:latest .
docker push grand512/grpc-sensor-server:latest
kubectl delete deployment sensor-void-energy-server
kubectl apply -f deployment.yaml