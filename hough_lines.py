import imutils
import numpy as np
import cv2


img = cv2.imread('breaths_mask.png')
ratio = img.shape[0] / 500.0
img = imutils.resize(img, height = 500)

output = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

minLineLength=100
lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=200)
# ensure at least some lines were found
if lines is not None:
	a,b,c = lines.shape
	for i in range(a):
		cv2.line(output,(lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
    
	cv2.imshow("output", np.hstack([img, output]))
	cv2.waitKey(0)

	