#coding=UTF-8
import base64
import json
from utils import * 

def read_captcha(img_byte):
    base64_data = base64.b64encode(img_byte)
    b64 = base64_data.decode()
    account_data = ReadJson('./config/tujian_account.json')
    data = {
        "username": account_data["username"], 
        "password": account_data["password"],
        "typeid": account_data["typeid"],
        "image": b64
    }
    result = json.loads(requests.post(url="http://api.ttshitu.com/predict", json=data).text)
    if result["success"]:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""