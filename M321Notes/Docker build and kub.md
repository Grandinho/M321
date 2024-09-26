docker build -t grand5120/minio-flask-app .
docker push grand5120/minio-flask-app
kubectl delete deployment minio-flask-app
kubectl apply -f .\deployment.yaml