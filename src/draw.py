import cv2

def draw_bbox(frame,list_box):
    for box in list_box:
        x,y,w,h = box
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
        # frame = cv2.rectangle(frame,(x,y),(x1,y1),(0,0,255))
    return frame