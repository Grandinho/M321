from minio import Minio
from flask import Flask

# host = "192.168.100.15:2016"
# bucket = "theship-permastore"
# access_key = "theship"
# secret_key = "theship1234"

# minio_client = Minio (
#     host,
#     access_key=access_key,
#     secret_key=secret_key,
#     secure=False
# )
# if minio_client.bucket_exists("theship-permastore"):
#     print('works')


from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')