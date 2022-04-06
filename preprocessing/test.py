import base64
import urllib.parse
import requests
import json
import timeit
import sys
import io
import cv2
import numpy as np
import time
import cProfile
start_time = time.time()
url = 'http://0.0.0.0:5002/predictBackGround'
# url = 'http://service.aiclub.cs.uit.edu.vn/face_anti_spoofing/predict/'
####################################
image_path = "output/test.jpg"
####################################
img = cv2.imread(image_path)
is_success, buffer = cv2.imencode('.png', img)
f = io.BytesIO(buffer)
image_encoded = base64.encodebytes(f.getvalue()).decode('utf-8')
####################################


# response = requests.post(url, data = data_json, headers=headers)
# response = response.json()
# print(response)
# print('time', time.time()-start_time)

THRESH_LIST = [1,3,5,10]

def main():
    cum = 0
    for i in range(100):
        # data ={"images": [image_encoded],'video_id':1,'frame_id':i,'THRESH_FRAME':THRESH_FRAME}
        data ={"image_path": image_path,'video_id':1,'frame_id':i}
        headers = {'Content-type': 'application/json'}
        data_json = json.dumps(data)
        response = requests.post(url, data = data_json, headers=headers)
        response = response.json()
        cum += response["data"]["process_time"]
    print(f" [Average:]",round(cum/100,5))
    # data ={"images": [image_encoded],'video_id':1}
    # headers = {'Content-type': 'application/json'}
    # data_json = json.dumps(data)
    # response = requests.post(url, data = data_json, headers=headers)
    # response = response.json()
if __name__ == '__main__':
    main()
    # cProfile.run('main()')