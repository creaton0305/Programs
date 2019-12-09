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
import time

#Path declaration/configuration
#document = open("/home/creaton/yolo_test2/testing.txt", "w")
#weights_path = '/home/creaton/yolo_test2/ourbestbestmodel.h5'
weights_path = '/home/creaton/yolo_test2/model_g5.h5'
config_path = '/home/creaton/yolo_test2/config.json'
image_name = 's0cm2 ' #Name of file
number_of_images = 500 + 1 #number of images you have to train + 1
int_width = 848
int_height = 464

#Get coordinates for objects
def get_coordinates(picture,box_info,labels):
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
    #    print(ID)
    #    print(dims)
    return dims,ID

#Create xml file
def create_xml(num_of_objects,labels,dimensions):
        #create file
        #open('/home/creaton/yolo_test2/xml_files/' + str(image_name) + str(index) + '.xml', "w+")

        #initialise xml
        xml_path = '/home/creaton/yolo_test2/actual_training/labels/' + str(image_name) + str(index_3d) + '.xml'
        root = Element("Annotation")
        tree = ElementTree(root)

        #Create filename tag
        filename = Element("filename")
        root.append(filename)
        filename.text=str(image_name) + str(index_3d) + '.jpg'

        #create photo size tag
        size = Element("size")
        root.append(size)

            #with tag in photo size
        width = Element("width")
        size.append(width)
        width.text=str(int_width)

            #height tag in photo size
        height = Element("height")
        size.append(height)
        height.text=str(int_height)

        #create object tag
        for x in range(0,num_of_objects):

            #object tag
            object = Element("object")
            root.append(object)

            #object name
            name = Element("name")
            object.append(name)
            name.text=str(labels[x])

            #bounding boxes coordinates
            bndbox = Element("bndbox")
            object.append(bndbox)

            #seperate coordinates into xmin,ymin,xmax,ymax
            xmin = Element("xmin")
            bndbox.append(xmin)
            xmin.text = str(dimensions[x][0])

            ymin = Element("ymin")
            bndbox.append(ymin)
            ymin.text = str(dimensions[x][1])

            xmax = Element("xmax")
            bndbox.append(xmax)
            xmax.text = str(dimensions[x][2])

            ymax = Element("ymax")
            bndbox.append(ymax)
            ymax.text = str(dimensions[x][3])

        tree.write(xml_path)

#YOLO setup
with open(config_path) as config_buffer:
    config = json.load(config_buffer)

yolo = YOLO(backend             = config['model']['backend'],
            input_size          = config['model']['input_size'],
            labels              = config['model']['labels'],
            max_box_per_image   = config['model']['max_box_per_image'],
            anchors             = config['model']['anchors'])

yolo.load_weights(weights_path)


for index in range(1,number_of_images): #do in batches

    index_3d = '%003d' % index
    #print(index_)
    image_path = '/home/creaton/yolo_test2/actual_training/images/' + str(image_name) + str(index_3d) + '.jpg'
    print(image_path)
    #image_path = '/home/creaton/yolo_test2/test_images/test4.jpg' #for test

    #Open image and find object in image
    image = cv2.imread(image_path)
    boxes = yolo.predict(image)

    #get bounding boxes coordinates
    dimensions = []
    object_name = []
    dimensions, object_name = get_coordinates(image,boxes,config['model']['labels'])
    num_of_objects = len(dimensions)

    #draw bounding boxes
    output_image = draw_boxes(image, boxes, config['model']['labels'])
    cv2.imshow('output', output_image)

    #create xml
    create_xml(num_of_objects, object_name, dimensions)

    time.sleep(1)

    k = cv2.waitKey(5) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
