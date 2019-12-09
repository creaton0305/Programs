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

pipeline = rs.pipeline()
configure = rs.config()
configure.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
configure.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(configure)

try:
	while True:
		frames = pipeline.wait_for_frames()
		color_frame = frames.get_color_frame()
		if not color_frame:
			continue

		color_image = np.array(color_frame.get_data())

		boxes = yolo.predict(color_image)
		obj = draw_boxes(color_image, boxes, config['model']['labels'])

		cv2.namedWindow("Just kill me already", cv2.WINDOW_AUTOSIZE)
		cv2.imshow("Murder me", color_image)
		cv2.waitKey(1)

		depth_frame = frames.get_depth_frame()
		data = depth_frame.get_data()
		data_array = np.array(data)

		dist_to_center = depth_frame.get_distance(int(depth_frame.get_width() / 2),int(depth_frame.get_height() / 2))
		print(dist_to_center)

finally:
	pipeline.stop()
