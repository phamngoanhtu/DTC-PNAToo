import cv2
import threading
import numpy as np
import Processor

class CAMERA(object):
    def __init__(self, camNum, camera_url, camName):
        self.camera_name = camName
        self.camera_num = camNum
        self.camera_url = camera_url
        self.person = []
        self.video = cv2.VideoCapture(self.camera_url)
        self.captureFrame  = None
        self.captureEvent = threading.Event()
        self.captureLock = threading.Lock()
        self.captureThread = threading.Thread(name='video_captureThread',target=self.get_frame)
        self.captureThread.start()
#        self.processor = Processor.ProcessoR(self)
        
    def get_frame(self):
        while True:
            success, frame = self.video.read()
            self.captureEvent.clear()
            if success:
                self.captureFrame  = frame.copy()
                self.captureEvent.set()
                
    def read_processed(self):
        with self.captureLock:
#             frame = self.processor.processing_frame
            frame = self.captureFrame
        while frame is None or not (type(frame) is np.ndarray):
            with self.captureLock:
                 #print("you're in read_processed_loop")
#                 frame = self.processor.processing_frame
                frame = self.captureFrame
        frame = frame.copy()
        r = 320.0 / frame.shape[1]
        dim = (320, 200)
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tostring()
        
