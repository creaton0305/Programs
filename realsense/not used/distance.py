from imutils import paths
import numpy as np
import imutils 
import cv2 

def distance_to_camera(knownWidth, focalLength, perWidth):
	#compute and return the distance from the maker to the camera
	return (knownWidth * focalLength)/perWidth
