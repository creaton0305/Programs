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

#global variables
x_centre_obj = []
y_centre_obj = []
obj_coords = []

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


#get coordinates for object 
def get_coordinates(pictures, box_info, labels):
	image_h, image_w, _ = pictures.shape 
	dims = []
	ID = []
	print(distance)	
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

#Find object with rgb camera
def find_object():
	

	#open RGB camera
	print("INFO: START FIND OBJECT")
	cap = cv2.VideoCapture(3)
	print("INFO: Link to camera done")
	
	#Set width and height of camera
	#set window width
	frameWidth = 640
	frameHeight = 480
	cap.set(3,frameWidth)
	cap.set(4,frameHeight)
	
	coordinates_dims = []
	coordinates_ID = []

	while cv2.waitKey(30) & 0xFF != ord('q'):	
	#capture frames from camera
		ret, rgb_frame = cap.read()

	#do prediction and get coordinates of object
		boxes = yolo.predict(rgb_frame)
		obj = draw_boxes(rgb_frame, boxes, config['model']['labels'])
		coordinates_dims,coordinates_ID = get_coordinates(rgb_frame, boxes, config['model']['labels'])
		#print(coordinates_dims)
		#print(coordinates_ID)

	#Show camera output
		cv2.imshow("RGB video", obj)

		if cv2.waitKey(30) & 0xFF == ord('q'):
			cap.release()		
			return coordinates_ID, coordinates_dims 
	
	
	#Close RGB Camera
	#cap.release()

	return coordinates_ID, coordinates_dims 
	

#Find distance with depth camera
def get_depth(x_coords, y_coords):
	
	#realsense setup
	pipeline = rs.pipeline()
	configure = rs.config()
	#configure.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
	configure.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	print("INFO: realsense set-up done")
	
	#Start streaming
	profile = pipeline.start(configure)
	print("INFO: Start streaming")

	#get depth frame for realsense
	frames = pipeline.wait_for_frames()
	print("INFO: waiting for frame")
	depth_frame = frames.get_depth_frame()
	print(depth_frame)
	print("INFO: got depth frame")
	#color_frame = frames.get_color_frame()
	#print("INFO: got color frame")
	if not depth_frame:
		print("WARNING: No frame received")
		print("KILLING PROCESS")
		return 

	#Convert color_frame to something readable for numpy and cv2
	data = depth_frame.get_data()
	data_array = np.array(data)
	
	#get distance
	dist_to_center = depth_frame.get_distance(int(x_coords),int(y_coords))

	#Show camera output
	cv2.imshow("depth video", np.array(depth_frame.get_data()))

	if cv2.waitKey(0) & 0xFF == ord('q'):
		return 
		
	return dist_to_center

#MAIN PROGRAM START
def main():	
	
	print("INFO: Going to sleep for 1 second")
	time.sleep(1)
	print("INFO: Wake up")
	
	dimensions = []
	object_name = []
	
	object_name, dimensions = find_object()
	print("Object name: ", object_name)
	print("Coordinates: ", dimensions)
	
	num_of_obj = len(object_name)
	for i in range(0,num_of_obj):
		y_centre_obj = (((dimensions[i][3] - dimensions[i][1])/2) + dimensions[i][1])
		x_centre_obj = (((dimensions[i][2] - dimensions[i][0])/2) + dimensions[i][0])
		print(x_centre_obj)
		print(y_centre_obj)		
		distance = get_depth(x_centre_obj, y_centre_obj)	
		#print(distance)
	
	#cv2.imshow('output', data_array)

	#if cv2. waitKey(30) & 0xFF == ord('q'):
	#	break

#	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
