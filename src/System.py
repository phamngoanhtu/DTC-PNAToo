import threading
import os
import cv2
import time
import socket
from PIL import Image
import io
import Camera

class System(object):
    def __init__(self):
        self.cameras = []
    
    def add_camera(self, camera):
        self.cameras.append(camera)
    def remove_camera(self, camID):
        self.cameras.pop(int(str(camID).strip('camera_')))
