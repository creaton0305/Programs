import cv2
import argparse
import os
import keras
import numpy as np
from tqdm import tqdm
from preprocessing2 import parse_annotation
from utils import draw_boxes,get_session
from frontend import YOLO
import json
import pyrealsense2 as rs 

#path declaration
weights_path = '/home/ashley/yolo_test2/ourbestbestmodel.h5'
config_path = '/home/ashley/yolo_test2/config.json'

#for green box to appear 
def get_coordinates(pictures, box_info, labels):
	image_h, image_w, _ = image.shape 
	dims = []
	ID = []
   
	for box in box_info:
		xmin = int(box.xmin*image_w)
		ymin = int(box.ymin*image_h)
		xmax = int(box.xmax*image_w)
		ymax = int(box.ymax*image_h)
		dims.append([xmin,ymin,xmax,ymax])
		ID.append(labels[box.get_label()])
		#print(ID)
		#print(dims)
	return dims,ID

with open(config_path) as config_buffer:
	config = json.load(config_buffer)

yolo = YOLO(backend             = config['model']['backend'],
	    input_size          = config['model']['input_size'],
	    labels              = config['model']['labels'],
	    max_box_per_image   = config['model']['max_box_per_image'],	
	    anchors             = config['model']['anchors'])

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(3)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

yolo.load_weights(weights_path)

while True:
	ret, frame = cap.read()
	
	boxes = yolo.predict(frame)
	obj = draw_boxes(frame, boxes, config['model']['labels'])
	cv2.imshow('output', obj)

	if cv2. waitKey(30) & 0xFF == ord('q'):
		break


cap.release()
cv2.destroyAllWindows()
