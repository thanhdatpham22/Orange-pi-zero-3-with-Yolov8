import requests
import json
import uuid
import csv
from data_csv import *
import threading

stop_event = threading.Event()

def push_server(roomStatus=1, roomPerson=0):
    # ------- sent request server--------------------------
    get_api = 'http://103.140.39.122/device/device/device?roomId=b4a9fcb839b3'
    put_api = 'http://103.140.39.122/device/device/device'
    roomId = hex(uuid.getnode())  # get MAC ADDRESS
    roomId = (str)(roomId)[2:]

    print (roomId)
    #roomNo = "3112"
    roomNo ="1201"
    roomName = 'Phong nghien cuu'
    #roomName ="Phòng lý thuyết"
    place = 'Tang 12-A1'
    #place = "Tòa A10"
    roomStatus = "1"
    roomPerson = "0"
    data_put = {'roomId': roomId, 'roomNo': roomNo, 'roomName': roomName, 'place': place, 'roomStatus': roomStatus,
                'roomPerson': roomPerson}
    #data_put = {'id': roomId, 'roomStatus': roomStatus,'roomPerson': roomPerson}
    # data_put['id'] = roomId
    # data_send = json.loads(data_put) # json to python
    # data_send = json.dumps(data_put) # python to json
    print(data_put)
    response = requests.put(put_api, json=data_put)  ## PUT service
    print(response)

    # print('reponse code:',response.status_code)
    get_response = requests.get(get_api)  # GET service
    print(get_response)
    print(get_response.json())
    #writer_csv('Database.csv', get_response.json())  # write data to csv file


if __name__ == '__main__':
    roomStatus = 1
    roomPerson = 0
    push_server(roomStatus, roomPerson)