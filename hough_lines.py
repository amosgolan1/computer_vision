import cv2
import numpy as np
import imutils

img = cv2.imread('images/breath_1.png')
ratio = img.shape[0] / 300.0
img = imutils.resize(img, height = 300)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur=cv2.GaussianBlur(gray, (11, 11), 0)

edges = cv2.Canny(gray,50,150)

# edges = cv2.Canny(blur,50,150,apertureSize = 3)

minLineLength = 1
maxLineGap = 1
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

for x1,y1,x2,y2 in lines[0]:
	cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
	print("line")
cv2.imshow('houghlines.png',img)	
cv2.imshow("edges", edges)
cv2.imshow("blur", blur)
cv2.waitKey(0)