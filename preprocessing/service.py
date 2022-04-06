import os
import io
import cv2
import time
import base64
import logging
import timeit
import datetime
import json

# import pydantic
# import uvicorn
# import asyncio
# import warnings
# import traceback
# import numpy as np
# from fastapi import FastAPI, File, UploadFile
# from fastapi.encoders import jsonable_encoder
# from typing import Optional, List
# from pydantic import BaseModel
# from configparser import ConfigParser
# import json
# import rcode
# import sys
# sys.path.append('../')

# warnings.filterwarnings('ignore')
# now = datetime.datetime.now()
# #######################################
# #####LOAD CONFIG####
# config = ConfigParser()
# config.read("config/service.cfg")

# SERVICE_IP = str(config.get('main', 'SERVICE_IP'))
# SERVICE_PORT = int(config.get('main', 'SERVICE_PORT'))
# LOG_PATH = str(config.get('main', 'LOG_PATH'))
# WORKER_NUM = str(config.get('main', 'WORKER_NUM'))
# MODEL = str(config.get('main', 'MODEL'))
# DEVICE_ID = int(config.get('main', 'DEVICE_ID'))
# THRESH_FRAME = int(config.get('main','THRESH_FRAME'))
# #######################################
# app = FastAPI()
# #######################################
# #####CREATE LOGGER#####
# os.makedirs(LOG_PATH, exist_ok=True)
# logging.basicConfig(filename=os.path.join(LOG_PATH, now.strftime("%d%m%y_%H%M%S")+".log"), filemode="w", level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# console = logging.StreamHandler()
# console.setLevel(logging.ERROR)
# logging.getLogger("").addHandler(console)
# logger = logging.getLogger(__name__)
# #######################################
# class Images(BaseModel):
#     data: Optional[List[str]] = pydantic.Field(default=None, example=None, description='List of base64 encoded images')
# class PredictData(BaseModel):
# #   images: Images
#     images: Optional[List[str]] = pydantic.Field(default=None, example=None, description='List of base64 encoded images')
#     video_id: str
#     frame_id: int
#     image_path: str
# #######################################
# print("SERVICE_IP", SERVICE_IP)
# print("SERVICE_PORT", SERVICE_PORT)
# print("LOG_PATH", LOG_PATH)
# print("WORKER_NUM", WORKER_NUM)
# print("API READY")
# #######################################

# THRESH = 200

# def decode(im_b64):
#     ### Decode as latin-1 ###
#     im_bytes = base64.b64decode(im_b64.replace('"',"'").encode('latin-1'))
#     im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
#     img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
#     return img

# def encode_img(img):
#     is_success, buffer = cv2.imencode('.png', img)
#     f = io.BytesIO(buffer)
#     image_encoded = base64.encodebytes(f.getvalue()).decode('utf-8')
#     return image_encoded

# @app.post('/predict')
# async def predict(data: PredictData):
#     ###################
#     #####
#     logger.info("predict")
#     return_result = {'code': '1001', 'status': rcode.code_1001}
#     ###################
#     try:
#         start_time = timeit.default_timer()
#         predicts = []
#         try:
#             images = jsonable_encoder(data.images)
#             return_result = "YESS"
#             for image in images:
#                 image_decoded = base64.b64decode(image)
#                 jpg_as_np = np.frombuffer(image_decoded, dtype=np.uint8)
#                 process_image = cv2.imdecode(jpg_as_np, flags=1)
#                 img,detection = pred(process_image)
#                 cv2.imwrite('./output/result.jpg',img)
#                 img = encode_img(img)
#                 predicts = [{"image":img,"label":detection}]
#             return_result = {'code': '1000', 'status': rcode.code_1000, 'data': {'predicts': predicts,
#                             'process_time': timeit.default_timer()-start_time, 'WORKER_NUM': WORKER_NUM}}
#         except Exception as e:
#             print(str(e))
#             print(str(traceback.print_exc()))
#             return_result = {'code': '609', 'status': rcode.code_609}
#             return; 
#         ###########################
#     except Exception as e:
#             logger.error(str(e))
#             logger.error(str(traceback.print_exc()))
#             return_result = {'code': '1001', 'status': rcode.code_1001}
#     finally:
#         return return_result

# json_data = json.load(open('Traffic-CongHoa-Truong-Chinh.json'))
# background = decode(json_data['DuongBaTrac-TaQuangBuu1 2017-07-18_08_00_00_000.asf'])

from kafka_messenger import KafkaProducer, KafkaConsumer

SCHEMA_REGISTRY = 'http://schema-registry:8080'

def process():
    consumer = KafkaConsumer('raw_frames')
    producer = KafkaProducer('processed_frames')
    while True:
        msg = consumer.consume()

        if msg is None:
            continue

        key = msg.key()
        value = msg.value()
        img = cv2.imread(value['url'])

        producer.produce(key=key, value=value)
    
# @app.post('/predictBackGround')
# async def predict(data: PredictData):
#     ###################
#     #####
#     logger.info("predict")
#     return_result = {'code': '1001', 'status': rcode.code_1001}
#     ###################
#     try:
#         start_time = timeit.default_timer()
#         predicts = []
#         try:
#             if data.frame_id % THRESH_FRAME != 0:
#                 return_result = {'code': '1000', 'status': rcode.code_1000, 
#                             'data': {
#                             'detectObject':False,
#                             # 'predicts': predicts,
#                             'process_time': timeit.default_timer()-start_time, 'WORKER_NUM': WORKER_NUM}}
#                 return return_result
#             else:
#                 # ###### encode decode bas64 ######
#                 # image = jsonable_encoder(data.images)[0]
#                 # image_decoded = base64.b64decode(image)
#                 # jpg_as_np = np.frombuffer(image_decoded, dtype=np.uint8)
#                 # process_image = cv2.imdecode(jpg_as_np, flags=1)
#                 # video_id = data.video_id
#                 # #################################

#                 ############## Use path ###############
#                 image_path = data.image_path
#                 process_image = cv2.imread(image_path)
#                 #######################################
        
#                 # background = decode(json_data[video_id])
                
#                 process_image = cv2.resize(process_image, background.shape[0:2][::-1] ,interpolation = cv2.INTER_AREA)
                
#                 mask = np.array(process_image - background > THRESH)
#                 final_image = np.multiply(255,mask).astype(np.uint8)
#                 grayImage = cv2.cvtColor(final_image, cv2.COLOR_BGR2GRAY)
#                 (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
#                 val_counts = np.unique(blackAndWhiteImage,return_counts=True)[1]
#                 detectObject = False
#                 if val_counts[0]/val_counts[1] < 2.5:
#                     detectObject = True
#                 return_result = "YESS"

#                 return_result = {'code': '1000', 'status': rcode.code_1000, 
#                             'data': {
#                             'detectObject':detectObject,
#                             # 'predicts': predicts,
#                             'process_time': timeit.default_timer()-start_time, 'WORKER_NUM': WORKER_NUM}}
#         except Exception as e:
#             print(str(e))
#             print(str(traceback.print_exc()))
#             return_result = {'code': '609', 'status': rcode.code_609}
#             return; 
#         ###########################
#     except Exception as e:
#             logger.error(str(e))
#             logger.error(str(traceback.print_exc()))
#             return_result = {'code': '1001', 'status': rcode.code_1001}
#     finally:
#         return return_result

if __name__ == '__main__':
    # uvicorn.run(app, port=SERVICE_PORT, host=SERVICE_IP,debug=True)
    process()
