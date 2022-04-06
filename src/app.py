from flask import Flask, render_template, url_for, send_file, Response, jsonify, send_file, request
# from model import main
import os
import cv2
import json
import time
import plotly
import random
import folium
import pandas as pd
from time import sleep
import plotly.express as px
import atexit, plotly, plotly.graph_objs as go
from draw import draw_bbox
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pusher import Pusher
# from urllib.request import urlopen
# with urlopen('https://gist.githubusercontent.com/hrbrmstr/94bdd47705d05a50f9cf/raw/0ccc6b926e1aa64448e239ac024f04e518d63954/asia.geojson') as response:
#     asia = json.load(response)

##Socket graph
pusher = Pusher(
    app_id = "1307595",
    key = "5fcda7fc431248b78bb1",
    secret = "e410fc2100dc881873dd",
    cluster = "ap1",
    ssl=True
)
app = Flask(__name__)

times,moto,car,bus,truck = [],[],[],[],[]
times2,moto2,car2,bus2,truck2 = [],[],[],[],[]
choice_graph = False
start = time.time()

def retrieve_data():
    times.append(time.strftime('%H:%M:%S'))
    moto.append(random.randint(15,25))
    bus.append(random.randint(2,5))
    car.append(random.randint(5,15))
    truck.append(random.randint(2,5))
    global choice_graph,start
    if len(times) > 8:
        times.pop(0)
        moto.pop(0)        
        car.pop(0)        
        bus.pop(0)
        truck.pop(0)        
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=truck,stackgroup='one',name='truck')) # fill down to xaxis
    fig.add_trace(go.Scatter(x=times, y=bus,stackgroup='one',name='bus')) # fill to trace0 y
    fig.add_trace(go.Scatter(x=times, y=car,stackgroup='one',name='car')) # fill down to xaxis
    fig.add_trace(go.Scatter(x=times, y=moto,stackgroup='one',name='motobike')) # fill down to xaxis
    
    ## Graph 2
    # trigger event
    times2.append(time.strftime('%H:%M:%S'))
    moto2.append(random.randint(30,50))
    bus2.append(random.randint(5,15))
    car2.append(random.randint(15,40))
    truck2.append(random.randint(7,15))
    if len(times2) > 8:
        times2.pop(0)
        moto2.pop(0)        
        car2.pop(0)        
        bus2.pop(0)
        truck2.pop(0)        
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=times, y=truck2,stackgroup='one',name='truck')) # fill down to xaxis
    fig2.add_trace(go.Scatter(x=times, y=bus2,stackgroup='one',name='bus')) # fill to trace0 y
    fig2.add_trace(go.Scatter(x=times, y=car2,stackgroup='one',name='car')) # fill down to xaxis
    fig2.add_trace(go.Scatter(x=times, y=moto2,stackgroup='one',name='motobike')) # fill down to xaxis
    
    fig.update_yaxes(range=[0, 110])
    fig2.update_yaxes(range=[0, 110])

    if choice_graph:
        start = time.time()
        graphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    if time.time() - start > 7:
        choice_graph = False
    data = {
        'graph': graphJSON,
    }

    pusher.trigger("crypto", "data-updated", data)


# @app.route('/check', methods=['GET', 'POST'])
# def check():
#     id = request.form['username']
#     print(id)
#     return "OK"
    
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ajax', methods = ['GET'])
def ajax_request():
    cam_id = request.args.get("cam_id")
    global choice_graph
    choice_graph = True
    return 'OK'
    

def listen(ip):
    cap = cv2.VideoCapture(f'./Videos/{ip}.mp4')
    count = 0
    while True:
        _,frame = cap.read()
        count += 1
        if count % 3 != 0:
            continue
        ###Back-end
        # draw_bbox(frame,bbox)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream/<ip>',methods=['GET'])
def stream(ip):
    return Response(listen(ip), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/thumbnail/<ip>/frame.jpg')
def thumbnail(ip):
    # cap = cv2.VideoCapture(f'./Videos/{ip}.mp4')
    # sleep(0.5)
    # ret,frame = cap.read()
    # cv2.imwrite(f'./feed/{ip}.jpg',frame)
    return send_file("feed/" + str(ip) + ".jpg", mimetype='image/jpg')

@app.route('/map')
def map():
    return send_file("feed/map/map.png", mimetype='image/jpg')

@app.route('/map_2')
def well_map():
    start_coords = [10.872989, 106.765281]
    folium_map = folium.Map(location=start_coords, zoom_start=20)
    return folium_map._repr_html_()

if __name__ == '__main__':
    # create schedule for retrieving prices
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=retrieve_data,
        trigger=IntervalTrigger(seconds=2),
        id='prices_retrieval_job',
        name='Retrieve prices every 10 seconds',
        replace_existing=False)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown()) 
    app.run(host='0.0.0.0', port=5000)
