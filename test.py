#!/usr/bin/env python3

from pickletools import uint1
import cv2
import math
import numpy as np

canvas = np.zeros((400,600,3),np.uint8)
canvas.fill(255)

while(1):
    #cv2.ellipse(canvas, (100,200), (50,100), 45, 0, 360, (150,150,0), 3)
    cv2.ellipse(canvas, (300,200), (100,50), 90, 0, 360, (150,150,0), 3)
    #cv2.ellipse(canvas, (500,200), (50,100), 315, 0, 360, (150,150,0), 3)
    cv2.imshow('Canvas', canvas)

    if cv2.waitKey(1) == ord('q'):
        break
        
cv2.destroyAllWindows()