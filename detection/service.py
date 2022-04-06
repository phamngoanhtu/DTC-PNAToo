import cv2
import json
import requests

from detect_api import *

from kafka_messenger import KafkaProducer, KafkaConsumer

if __name__ == '__main__':
    consumer = KafkaConsumer('processed_frames')
    producer = KafkaProducer('det_results')
    while True:
        msg = consumer.consume()

        if msg is None:
            continue

        key = msg.key()
        value = msg.value()

        frame_id = value['frame_id']
        img_path = value['url']
        img = cv2.imread(img_path)
        
        img, detection = inference(img)
        # detection = [[x1, y1, x2, y2, score, class], ...]

        bbox = [bb[:4] for bb in detection]
        score = [bb[4] for bb in detection]
        classes = [bb[5] for bb in detection]
        
        producer.produce(
            key=key, 
            value={
                'frame_id': frame_id,
                'score': score,
                'class': classes,
                'bbox': bbox,
            }
        )