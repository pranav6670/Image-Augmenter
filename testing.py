import cv2
import os
import numpy as np

image = cv2.imread('test.jpeg', 1)
b, g, r = cv2.split(image)

# cv2.imshow('b', b)
# cv2.imshow('g', g)
# cv2.imshow('r', r)

cv2.waitKey(0)
cv2.destroyAllWindows()