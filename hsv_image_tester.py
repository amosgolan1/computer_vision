from __future__ import print_function
import cv2 as cv2
import argparse
import imutils
from imutils.video import VideoStream

from imutils.video import FPS
import imutils

 

from collections import deque
import numpy as np
import argparse

import time

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
# uncomment if using video
# window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'

window_capture_name = 'image Capture'


low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
def on_low_H_thresh_trackbar(val):
	global low_H
	global high_H
	low_H = val
	low_H = min(high_H-1, low_H)
	cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
	global low_H
	global high_H
	high_H = val
	high_H = max(high_H, low_H+1)
	cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
	global low_S
	global high_S
	low_S = val
	low_S = min(high_S-1, low_S)
	cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
	global low_S
	global high_S
	high_S = val
	high_S = max(high_S, low_S+1)
	cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
	global low_V
	global high_V
	low_V = val
	low_V = min(high_V-1, low_V)
	cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
	global low_V
	global high_V
	high_V = val
	high_V = max(high_V, low_V+1)
	cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)
parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
# parser.add_argument("-v", "--video", required=True,
# 	help="path to input video file")
parser.add_argument("-i", "--image", required=True,
	help="path to input image file")

args = parser.parse_args()

# cap = cv.VideoCapture(args.camera)
# cap = cv2.VideoCapture(args.video)
while(1):
# uncomment for image
	# image = cv2.imread(args.image,cv.IMREAD_COLOR)
	image = cv2.imread(args.image)
	ratio = image.shape[0] / 300.0
	orig = image.copy()
	image = imutils.resize(image, height = 300)
	# give image a new name to fit with the rest of the code
	frame = image
# fps = FPS().start()


	cv2.namedWindow(window_capture_name)
	cv2.namedWindow(window_detection_name)
	cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
	cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
	cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
	cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
	cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
	cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)



# while True:
# 	# uncomment for video
# 	# print("while loop")
# 	ret, frame = cap.read()
# 	if frame is None:
# 		break

	frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
		
	print(low_H, low_S, low_V)

	frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
	frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
	
	
	cv2.imshow(window_capture_name, frame)
	cv2.imshow(window_detection_name, frame_threshold)


	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	edged = cv2.Canny(gray, 30, 200)
	cv2.imshow("Edged", edged)
	cv2.waitKey(0)
cv.destroyAllWindows()
	# key = cv2.waitKey(30)
	# if key == ord('q') or key == 27:
	# 	break


