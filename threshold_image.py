# import the necessary packages
import argparse
import cv2
import imutils
import time

t=128

def nothing(x):
	# print("Trackbar value: " + str(x))
	pass

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be thresholded")
# ap.add_argument("-t", "--threshold", type = int, default = 128,
# 	help = "Threshold value")
args = vars(ap.parse_args())
 
# load the image and convert it to grayscale
image = cv2.imread(args["image"])
image = imutils.resize(image, width=450)

window_name = "Threshold calibrator"
cv2.namedWindow(window_name)
cv2.createTrackbar('threshold',window_name,0,255,nothing)
cv2.setTrackbarPos('threshold',window_name, t)
font = cv2.FONT_HERSHEY_SIMPLEX


# initialize the list of threshold methods

while(1):	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)

	(T, thresh) = cv2.threshold(gray, t, 255,cv2.THRESH_BINARY)
	cv2.imshow(window_name,thresh)
		# thr
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break
		# get current positions of Upper HSV trackbars
	t = cv2.getTrackbarPos('threshold',window_name)
	time.sleep(.1)

cv2.destroyAllWindows()
