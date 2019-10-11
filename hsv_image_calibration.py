# a script to test hsv values on an image from the computer

import numpy as np
import cv2 as cv
import time
from imutils.video import VideoStream
import argparse
from imutils.video import FPS
import imutils


img = cv.imread('b1.png',cv.IMREAD_COLOR)
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image")
args = vars(ap.parse_args())
img = cv.imread(args["image"],cv.IMREAD_COLOR)

ratio = img.shape[0] / 300.0
img = imutils.resize(img, height = 300)
img = cv.medianBlur(img,5)

# Convert BGR to HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

uh = 20
us = 130
uv = 180
lh = 0
ls = 50
lv = 100
lower_hsv = np.array([lh,ls,lv])
upper_hsv = np.array([uh,us,uv])

# Threshold the HSV image to get only blue colors
mask = cv.inRange(hsv, lower_hsv, upper_hsv)

window_name = "HSV Calibrator"
cv.namedWindow(window_name)

def nothing(x):
	print("Trackbar value: " + str(x))
	pass

# create trackbars for Upper HSV
cv.createTrackbar('UpperH',window_name,0,255,nothing)
cv.setTrackbarPos('UpperH',window_name, uh)

cv.createTrackbar('LowerH',window_name,0,255,nothing)
cv.setTrackbarPos('LowerH',window_name, lh)

cv.createTrackbar('UpperS',window_name,0,255,nothing)
cv.setTrackbarPos('UpperS',window_name, us)

cv.createTrackbar('LowerS',window_name,0,255,nothing)
cv.setTrackbarPos('LowerS',window_name, ls)

cv.createTrackbar('UpperV',window_name,0,255,nothing)
cv.setTrackbarPos('UpperV',window_name, uv)

cv.createTrackbar('LowerV',window_name,0,255,nothing)
cv.setTrackbarPos('LowerV',window_name, lv)

font = cv.FONT_HERSHEY_SIMPLEX

while(1):
	# Threshold the HSV image to get only light brown colors of the box
	mask = cv.inRange(hsv, lower_hsv, upper_hsv)
	mask1 = mask.copy() 
	image = img.copy()
	cv.putText(mask,'Lower HSV: [' + str(lh) +',' + str(ls) + ',' + str(lv) + ']', (10,30), font, 0.5, (200,255,155), 1, cv.LINE_AA)
	cv.putText(mask,'Upper HSV: [' + str(uh) +',' + str(us) + ',' + str(uv) + ']', (10,60), font, 0.5, (200,255,155), 1, cv.LINE_AA)

	cv.imshow(window_name,mask)
	# cv.imshow("main course box", img)

	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	gray = cv.bilateralFilter(gray, 11, 17, 17)
	edged = cv.Canny(gray, 30, 200)
	cv.imshow("Edged image", edged)

	edged_from_mask_deliated = cv.Canny(cv.erode(cv.dilate(mask1, None, iterations=5),None, iterations=15),30,20)
	edged_from_mask = cv.Canny(mask1, 30, 200)
	# cv.imshow("Edged from mask", edged_from_mask)
	cv.imshow("Edged from mask eroded and dilated prior", edged_from_mask_deliated)
	


	
# this part is here to find rectangles find contours in the edged and deliated image, keep only the largest ones which are the boxes
# compare the box area to the knwon are of the box in the future (caculate this)
# 

	cnts = cv.findContours(edged_from_mask_deliated.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv.contourArea, reverse = True)[:3]
	boxCnt = None

	# loop over our found  contours
	for c in cnts:
		# approximate the contour
		peri = cv.arcLength(c, True)
		approx = cv.approxPolyDP(c, 0.05 * peri, True)
	 
		# if our approximated contour has four points, then
		# we can assume that we have found our box. change this code to find more then one box
		if len(approx) == 4:
			screenCnt = approx
			# print("found")
			break


	cv.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
	cv.imshow("rectangle", image)
	# cv.waitKey(0)



	k = cv.waitKey(1) & 0xFF
	if k == 27:
		break
	# get current positions of Upper HSV trackbars
	uh = cv.getTrackbarPos('UpperH',window_name)
	lh = cv.getTrackbarPos('LowerH',window_name)
	us = cv.getTrackbarPos('UpperS',window_name)
	ls = cv.getTrackbarPos('LowerS',window_name)
	uv = cv.getTrackbarPos('UpperV',window_name)
	lv = cv.getTrackbarPos('LowerV',window_name)
	

	upper_hsv = np.array([uh,us,uv])
	lower_hsv = np.array([lh,ls,lv])

	time.sleep(.1)

cv.destroyAllWindows()
