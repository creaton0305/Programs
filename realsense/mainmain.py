#sudo modprobe uvcvideo nodrop=1 timeout=5000
#sudo rmmod uvcvideo

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
import time

#path declaration
weights_path = '/home/ashley/yolo_test2/ourbestbestmodel.h5'
config_path = '/home/ashley/yolo_test2/config.json'

#get coordinates for object 
def get_coordinates(pictures, box_info, labels):
	image_h, image_w, _ = pictures.shape 
	dims = []
	ID = []
	for box in box_info:	
		xmin = int(box.xmin*image_w)
		ymin = int(box.ymin*image_h)
		xmax = int(box.xmax*image_w)
		ymax = int(box.ymax*image_h)
		dims.append([xmin,ymin,xmax,ymax])
		ID.append(labels[box.get_label()])
		#print("ID: ", ID)		
		#print("Coords: ", dims)
		
	return dims, ID

#START PROGRAM
#yolo stuff
with open(config_path) as config_buffer:
	config = json.load(config_buffer)

yolo = YOLO(backend             = config['model']['backend'],
	    input_size          = config['model']['input_size'],
	    labels              = config['model']['labels'],
	    max_box_per_image   = config['model']['max_box_per_image'],	
	    anchors             = config['model']['anchors'])

yolo.load_weights(weights_path)
print("INFO: YOLO setup done")

	
#realsense setup
pipeline = rs.pipeline()
configure = rs.config()
configure.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
configure.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
print("INFO: realsense set-up done")

#Start streaming
profile = pipeline.start(configure)
print("INFO: Start streaming")

while True:	

	#get depth frame for realsense
	frames = pipeline.wait_for_frames()
	print("INFO: waiting for frame")

	color_frame = frames.get_color_frame()
	print("INFO: Received color frame")
	depth_frame = frames.get_depth_frame()
	print("INFO: Received depth frame")

	if not color_frame:
		print("WARNING: No frame received")
		print("KILLING PROCESS")
		break

	#Convert color_frame to something readable for numpy and cv2
	color_frame_data = color_frame.get_data()
	color_image = np.array(color_frame_data)
	depth_frame_data = depth_frame.get_data()
	depth_image = np.array(depth_frame_data)

	#find object and get coordinates of object
	boxes = yolo.predict(color_image)
	obj = draw_boxes(color_image, boxes, config['model']['labels'])
	coordinates_dims,coordinates_ID = get_coordinates(color_image, boxes, config['model']['labels'])
	print(coordinates_dims)
	print(coordinates_ID)
	
	num_of_obj = len(coordinates_ID)	
	
	for i in range(0,num_of_obj):
		y_centre_obj = (((coordinates_dims[i][3] - coordinates_dims[i][1])/2) + coordinates_dims[i][1])
		x_centre_obj = (((coordinates_dims[i][2] - coordinates_dims[i][0])/2) + coordinates_dims[i][0])
		#print(x_centre_obj)
		#print(y_centre_obj)		

		#get distance 
		dist_to_object_center = depth_frame.get_distance(int(x_centre_obj),int(y_centre_obj))
		print(dist_to_object_center)

	#Show camera output
	cv2.imshow("RGB video", color_image)
	cv2.imshow("depth video", depth_image)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
cv2.destroyAllWindows()
