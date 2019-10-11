import cv2 as cv
import numpy as np
import imutils 
cap = cv.VideoCapture(0)
# h=rawInput("Enter hue value")
v_lower=int(input("enter v lower value"))
s_upper = int(input("enter s upper value"))



while(1):
  
    # Take each frame
    _, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV

    lower_blue = np.array([0,0,255-v_lower])
    upper_blue = np.array([255,s_upper,255])

    # lower_blue = np.array([110,50,50])
    # upper_blue = np.array([130,255,255])
    # define range of red color in HSV
    lower_red = np.array([50,50,110])
    upper_red = np.array([255,255,130])

    # Threshold the HSV image to get only blue colors
    mask1 = cv.inRange(hsv, lower_blue, upper_blue)
    # mask2 = cv.inRange(hsv, lower_red, upper_red)
    # Bitwise-AND mask and original image
    blue_mask = cv.bitwise_and(frame,frame, mask= mask1)
    # red_mask = cv.bitwise_and(frame, frame, mask= mask2)

    cv.imshow('frame',frame)
    cv.imshow('mask',mask1)
    # cv.imshow('mask',mask2)
    cv.imshow('blue_mask',blue_mask)
    # cv.imshow('red_mask',red_mask)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()