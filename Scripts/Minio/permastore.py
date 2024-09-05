from minio import Minio

host = "192.168.100.15:2016"
bucket = "theship-permastore"
access_key = "theship"
secret_key = "theship1234"

minio_client = Minio (
    host,
    access_key=access_key,
    secret_key=secret_key,
    secure=False
)

minio_client.make_bucket("theship-permastore")