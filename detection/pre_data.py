import os
import re
import glob
import random

paths = glob.glob('../../mapr/vehicle_data/day/*.jpg')
matches = ["cam_01","cam_03","cam_14","cam15"]
path_imgs = []

for path in paths:
    if not any(x in path.split('/')[-1] for x in matches):
        path_imgs.append(path)
# path_imgs += glob.glob('../../mapr/vehicle_data/data_khoa/Img/5*.jpg')
path_imgs += glob.glob('../../mapr/vehicle_data/data_khoa/Img/cam_01*.jpg')
path_imgs += glob.glob('../../mapr/vehicle_data/data_khoa/Img/cam_14*.jpg')
# path_imgs = sorted(path_imgs)
out = ''
random.shuffle(path_imgs)

path_imgs_test = path_imgs[:int(len(path_imgs)*0.2)]
path_imgs_train = path_imgs[int(len(path_imgs)*0.2):]
for path in path_imgs_train:
    out+=path+'\n'
with open('train.txt','w+') as f:
    f.write(out)
out = ''
for path in path_imgs_test:
    out+=path+'\n'
with open('test.txt','w+') as f:
    f.write(out)
print(len(path_imgs_train) + len(path_imgs_test))
print(len(path_imgs),len(path_imgs_train),len(path_imgs_test))