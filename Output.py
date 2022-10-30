#!/usr/bin/env python3

from tkinter import image_names
import cv2
import numpy as np

def switchOutput(background, camera_image):
    counter= False

    while True:
        image_flip=camera_image

        mask = cv2.inRange(background,(0,0,0),(0,0,255))
        mask = mask.astype(bool)

        if counter:
            image_flip[mask] = background[mask]  #! joins the circle and the camera image

        k = cv2.waitKey(1)
        if k == 27:
            cv2.destroyAllWindows()
            break
        if k == ord('v'):
            counter = not counter
            print('Switched Output')
