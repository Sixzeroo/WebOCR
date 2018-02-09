import os,platform

upload_path = os.path.join(os.path.dirname(__file__), "img")
static_path = os.path.join(os.path.dirname(__file__), "static")

APP_ID = 'XXXXXXXX'
API_KEY = 'XXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXX'

IP = '127.0.0.1'
if(platform.system() == 'Linux'):
    IP = '0.0.0.0'
PORT = 8080
