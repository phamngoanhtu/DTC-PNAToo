import argparse
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import torch
import glob
import torch.backends.cudnn as cudnn

FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, colorstr, non_max_suppression, \
    scale_coords, xyxy2xywh,  set_logging, increment_path
from utils.plots import colors, plot_one_box
from utils.torch_utils import select_device, time_sync
from utils.augmentations import letterbox


@torch.no_grad()
def load_model():
    set_logging()
    device = select_device('6')
    half = False
    half &= device.type != 'cpu'

    weights = 'runs/train/day_5s/weights/best.pt'
    w = weights[0] if isinstance(weights, list) else weights
    classify, suffix = False, Path(w).suffix.lower()
    pt, onnx, tflite, pb, saved_model = (suffix == x for x in ['.pt', '.onnx', '.tflite', '.pb', ''])  # backend
    stride, names = 64, [f'class{i}' for i in range(1000)]  # assign defaults
    if pt:
        model = attempt_load(weights, map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        names = model.module.names if hasattr(model, 'module') else model.names  # get class names
        if half:
            model.half()  # to FP16
    return model
model = load_model()
device = select_device('6')   
names = model.module.names if hasattr(model, 'module') else model.names
model(torch.zeros(1, 3, *[640,640]).to(device).type_as(next(model.parameters())))

def load_img(img0, img_size, stride, auto=True):
    # Padded resize
    img = letterbox(img0, img_size, stride=stride, auto=auto)[0]
    # Convert
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    img = np.ascontiguousarray(img)

    return (img, img0)

# @torch.no_grad()
def inference(img_raw,model=model,imgsz=[640,640],  # inference size (pixels)
        conf_thres=0.05,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,
        half = False,
        agnostic_nms=False,  # class-agnostic NMS
        augment=False, hide_labels=False,  # hide labels
        hide_conf=False, ):

    pt = True
    classes = None
    stride = 64
    imgsz = check_img_size(imgsz, s=stride)

    start = time.time()
    img, im0s = load_img(img_raw,img_size=640, stride=stride, auto=pt)
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img = img / 255.0 
    if len(img.shape) == 3:
        img = img[None]
    # print(time.time() - start,'time pre')
    # Inference
    start = time.time()
    t0 = time.time()
    pred = model(img, augment=augment, visualize=False)[0]
    # print(time.time()-start,'time predict')
    # NMS
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
    t2 = time_sync()
    # Process predictions
    start = time.time()
    for i, det in enumerate(pred): 
        im0 = im0s.copy()

        s = '%gx%g ' % img.shape[2:]  # print string
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        imc = im0  # for save_crop
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

            # Write results
            predict = []
            for *xyxy, conf, cls in reversed(det):
                c = int(cls)
                x1,y1,x2,y2 = int(xyxy[0]),int(xyxy[1]),int(xyxy[2]),int(xyxy[3])
                predict.append([x1,y1,x2,y2,round(float(conf),4),c])
                # label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                # im0 = plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_width=1)
        # cv2.imwrite('./result/result.jpg', im0)
        # print(time.time()-start,'time processing')
        # print(f'Done. ({t2 - t0:.3f}s)')
    return 'path',predict

# source = glob.glob('../../mapr/vehicle_data/day/*.jpg')[:10]
# img = cv2.imread(source[0])
# inference(model,img)
