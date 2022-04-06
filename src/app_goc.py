import cv2
import requests
import json
import time
import numpy as np

import queue
import threading

SCHEMA_REGISTRY = 'http://schema-registry:8080'
# Wait until Schema Registry is online
while True:
    try:
        _ = requests.get(SCHEMA_REGISTRY)
        break
    except requests.exceptions.RequestException:
        pass

from kafka_manager import create_topics, create_schema
from kafka_messenger import KafkaProducer, KafkaConsumer

# video_list = [(str(video_id), queue.Queue(), [0], \
    # cv2.VideoCapture('rtsp://label:label123@192.168.28.30:5000/mystream')) for video_id in range(1)]
video_list = [(str(video_id), queue.Queue(), [0], [np.zeros((720, 1280, 3), dtype=np.uint8)], \
    cv2.VideoCapture('/Videos/DuongBaTrac-TaQuangBuu1 2017-07-18_08_00_00_000.asf'.format(video_id))) for video_id in range(10)]

def receive_video_stream(video_id):
    _, q, _, _, cap = video_list[video_id]
    while True:
        ret, frame = cap.read()
        if not ret: continue
        q.put(frame)
        # time.sleep(1/15)

def receive_track_results():
    while True:
        msg = tracking_consumer.consume()

        if msg is None:
            continue

        print("Tracking:", msg.value())

def receive_count_results():
    while True:
        msg = counting_consumer.consume()

        if msg is None:
            continue

        print("Counting:", msg.value(), flush=True)

def process(video_id):
    global video_list

    start_time = time.time()

    producer = KafkaProducer('raw_frames')

    MAX_FRAME = 1000
    video_id, q, frame_id, current_frame, _ = video_list[video_id]
    while frame_id[0] < MAX_FRAME:
        if q.empty(): continue
        frame = q.get()

        frame_id[0] += 1

        detect = frame_id[0] % 3 == 0

        current_frame[0] = frame

        if detect:
            image_path = '/storage/{}_{:05d}.jpg'.format(video_id, frame_id[0])
            cv2.imwrite(image_path, frame)

            value = {"frame_id": frame_id[0], "url": image_path}

            producer.produce(key=video_id, value=value)
            # producer.flush()

    producer.flush()
    print("io time:", time.time() - start_time, flush=True)

    counting_consumer = KafkaConsumer('count_results')
    n=0
    while True:
        msg = counting_consumer.consume()

        if msg is None:
            break

        n += 1
        if n % 500 == 0:
            print(n, time.time() - start_time, flush=True)

    print("Processed {} frames".format(sum([x[2][0] for x in video_list])))
    print("Processing time:", time.time() - start_time)

from flask import Flask, render_template, Response
app = Flask(__name__)

def gen_frames(camera_id):
    while True:
        frame = video_list[camera_id][3][0]
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed/<int:list_id>/', methods=["GET"])
def video_feed(list_id):
    return Response(gen_frames(camera_id=list_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=["GET"])
def index():
    return render_template('player.html')

if __name__ == '__main__':
    create_topics()
    create_schema()

    time.sleep(20)

    # Receive()

    thread_receive_stream = []
    for i, _ in enumerate(video_list):
        thread_receive_stream.append(threading.Thread(target=receive_video_stream, args=[i]))
    
    # p2 = threading.Thread(target=receive_tracking)
    # p3 = threading.Thread(target=receive_counting)

    thread_process = []
    for i, _ in enumerate(video_list):
        thread_process.append(threading.Thread(target=process, args=[i]))

    for thread in thread_receive_stream:
        thread.start()
    
    for thread in thread_process:
        thread.start()

    app.run(host='0.0.0.0', port=8000)

    for thread in thread_receive_stream:
        thread.join()