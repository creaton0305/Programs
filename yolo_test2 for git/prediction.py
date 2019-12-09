import cv2
import argparse
import os
import cv2
import keras
import numpy as np
from tqdm import tqdm
from preprocessing2 import parse_annotation
from utils import draw_boxes,get_session
from frontend import YOLO
import json
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

#Path declaration
#document = open("/home/creaton/yolo_test2/testing.txt", "w")
#weights_path = '/home/creaton/yolo_test2/ourbestbestmodel.h5'
weights_path = '/home/creaton/yolo_test2/model_g3.h5'
#weights_path = '/home/creaton/yolo_test2/model_g2.h5'
config_path = '/home/creaton/yolo_test2/config.json'
image_path = '/home/creaton/yolo_test2/test_images/test8.jpg' #Name of file
#image_path = '/home/creaton/yolo_test2/actual_training/images/s0cm 263.jpg' #Name of file
with open(config_path) as config_buffer:
    config = json.load(config_buffer)

yolo1 = YOLO(backend             = config['model']['backend'],
            input_size          = config['model']['input_size'],
            labels              = config['model']['labels'],
            max_box_per_image   = config['model']['max_box_per_image'],
            anchors             = config['model']['anchors'])

yolo1.load_weights(weights_path)

image = cv2.imread(image_path)
#resize = cv2.resize(image,(360, 640))
boxes1 = yolo1.predict(image)

test1 = draw_boxes(image, boxes1, config['model']['labels'])

resize1 = cv2.resize(test1, (360,640))

cv2.imshow('model1', resize1)
#cv2.imshow('model2', resize2)
#cv2.imshow('model3', resize3)

k = cv2.waitKey(0)

cv2.destroyAllWindows()
