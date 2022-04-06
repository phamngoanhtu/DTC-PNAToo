import cv2
import threading
import socket
import io
import base64
import ast
import colorsys

import os
import numpy as np
import time
from PIL import Image

class ProcessoR():
    def __init__(self, camera):
        print("init Processor")
        self.camera = camera
        self.processing_frame = None
        self.processingThread = threading.Thread(name='frame_processingThread',target=self.drawInFrame)
        self.processingThread.start()
    
    def drawInFrame(self):
        while True:
            if self.camera.captureFrame is not None:
                self.processing_frame = self.camera.captureFrame.copy()
#                cv2.rectangle(self.processing_frame,(0,0),(100,100),(0,255,0),3)
                
                    
