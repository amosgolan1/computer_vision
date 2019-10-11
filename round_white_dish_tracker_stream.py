# import the necessary packages
# think of using the HSL space instead as it is better suted for white color
# this example is looking for a white objectm and draws a circle around it. the object does not have to be round
# the code will detectsmaller objects and call them "side" and larger objects and call them antree
# think of incorporating a circle detection algorithem


from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

# sensitivity = 15

# whiteLower = (0, 0, 255-sensitivity)
# whiteUpper = (255, sensitivity, 255)

# change this to work well with our plate color
whiteLower = (0, 0, 120)
whiteUpper = (255, 30, 255)

# pts = deque(maxlen=args["buffer"])

vs = VideoStream(src=0).start()

# allow the camera or video file to warm up
time.sleep(2.0)
# keep looping
while True:
	# grab the current frame
	frame = vs.read()
 
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
 
	# # if we are viewing a video and we did not grab a frame,
	# # then we have reached the end of the video
	# if frame is None:
	# 	break
 
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, whiteLower, whiteUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		# c = max(cnts, key=cv2.contourArea)
		for c in cnts:
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	 
			# only proceed if the radius meets a minimum size
			# in the future, this needs to also check for a specific shape, like circle (plate) or the shape of the plates we use

			if radius > 70 and radius<85:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.putText(frame, "Side", (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255),lineType=cv2.LINE_AA )
				# cv2.circle(frame, center, 5, (0, 0, 255), -1)
			
			if radius > 90:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 0), 2)
				cv2.putText(frame, "Antree", (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255),lineType=cv2.LINE_AA ) 
				# cv2.circle(frame, center, 5, (0, 0, 255), -1)	

 
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
 
# otherwise, release the camera
else:
	vs.release()
 
# close all windows
cv2.destroyAllWindows()