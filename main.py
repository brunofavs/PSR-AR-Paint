#!/usr/bin/env python3

#-----------
# Conventions
#-----------

#! camelCase for functions and methods
#! snake_case for variables

#-----------
# Imports
#-----------
import argparse
import cv2
import numpy as np
from functools import partial
import json
import pprint
from copy import deepcopy
from collections import namedtuple

#-----------
# Global variables
#-----------

centroid_tuple = namedtuple('centroid_tupleeee',['x','y']) # No point in being a dictionary as I dont ever want to change the coordinates of the centroid
# First is the object name, the str is whats shown when printed

#-----------
# Functions
#-----------

def biggestBlob(masked_image):
#* Receives the unfiltered masked image and returns the mask with the biggest blob and it's centroid

    resolution = masked_image.shape # So that it can handle different cameras
    connectivity = 8 # Whether to check for the diagonal pixels or not, should be 4 if not considering diagonals
        
    # cv2.CV_8U stands for images with unsigned chars, which matchs the programm's needs
    cc_output_matrix = cv2.connectedComponentsWithStats(masked_image,connectivity,cv2.CV_8U)
    
    #* ---Dividing the output of CC into 1 int and 3 matrix's----
    cc_num_lables = cc_output_matrix[0]
    cc_labels = cc_output_matrix[1] 
    cc_stats = cc_output_matrix[2]
    cc_centroids = cc_output_matrix[3]

    #* ---Calculates a array with just the areas, excluding idx[0]----
    cc_areas = cc_stats[1:cc_num_lables,4]

    #* ---Getting the label number of the largest component----

    if cc_areas.size == 0 : # If there are no components, it should return a black mask


        empty_mask = np.zeros([resolution[0], resolution[1]],dtype = np.uint8)
        empty_bool_mask = empty_mask.astype(bool)

        centroid = centroid_tuple(x= -50,y=-50) # TODO check if this is valid later on

        return empty_mask,centroid; 
    else :
        max_label = cc_areas.argmax() + 1 # +1 because we're ignoring idx 0, bcs its background

    #* ---Calculates the mask with the biggest blob----

    cc_mask = np.zeros([resolution[0], resolution[1]],dtype = np.uint8) # Matrix of 0's 480x640

    cc_mask[cc_labels==max_label] = cc_labels[cc_labels==max_label] # Matrix with 0's and max label's number

    cc_mask_bool = cc_mask.astype(bool) # Matrix with 0's and 1's


    #* ---Calculates the centroid of the biggest blob----

    x,y = cc_centroids[max_label]
    centroid = centroid_tuple(x= int(x),y=int(y)) # Need casting because the image matrix is uint8

    
    return cc_mask,centroid
    
#-----------
# Main
#-----------

def main():
    #-----------------------------
    # Initialization
    #-----------------------------

    #* ---Configuration of argparse----
    parser = argparse.ArgumentParser(description='AR paint') 
    parser.add_argument('-usp','--use_shake_prevention', action='store_true',default = False ,help='Use shake mode : Prevents unintended lines across long distances')
    parser.add_argument('-j','--json',type=str,required=True,help='Absolute path for json file with color thresholds') 
    args = parser.parse_args()

    #* ---Loading json file into memory----
    json_inicial_object = open(args.json)
    color_boundaries = json.load(json_inicial_object)

    #* ---Setting up videoCapture object----
    capture_object = cv2.VideoCapture(0)  #! Camera images will be camera_src_img
    _,camera_source_img = capture_object.read() # Need this to configure resolution

    resolution = camera_source_img.shape


    #* ---Creating a blank image to drawn on---
    src_img = np.zeros([resolution[0], resolution[1], 3],dtype = np.uint8)
    src_img[:] = 255

    src_img_gui = deepcopy(src_img)

    #-----------------------------
    # Processing
    #-----------------------------

    #* ---Creating boundary arrays for masking---
    upper_bound_bgr = np.array([color_boundaries['limits']['B']['max'], color_boundaries['limits']['G']['max'], color_boundaries['limits']['R']['max']] )
    lower_bound_bgr = np.array([color_boundaries['limits']['B']['min'], color_boundaries['limits']['G']['min'], color_boundaries['limits']['R']['min']] )

    #* ---Creating windows---
    cv2.namedWindow("Camera Source",cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Mask",cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Biggest Object in Mask",cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Drawing")

    #* ---Configuring mouseCallback---
    #TODO mouseCallback

    while(1):

        #* ---Camera source image processing---
        _,camera_source_img = capture_object.read()
        camera_source_img = cv2.flip(camera_source_img,1) # Flip image on x-axis


        #* ---Masked image processing---
        masked_camera_image = cv2.inRange(camera_source_img,lower_bound_bgr,upper_bound_bgr) # Matrix of 0's and 255's

        #* ---Filtering the biggest blob in the image---

        cc_mask , cc_centroid = biggestBlob(masked_camera_image)
        cc_masked_camera_image = np.zeros([resolution[0], resolution[1]],dtype = np.uint8) # Matrix of 0's 480x640
         
        # TODO Check why the first approach didn't work
        # cc_masked_camera_image[cc_mask] = masked_camera_image[cc_mask]  # Matrix of 0's and 255's  480x640
        cc_masked_camera_image = np.where(cc_mask,masked_camera_image,0)  

        #* ---Drawing a x where the centroid is in the source---
        # TODO For now will just draw a circle

        cv2.circle(camera_source_img,cc_centroid,10,(0,0,255),-1)


        


        #-----------------------------
        # Visualization
        #-----------------------------

        #* ---Image showing---
        cv2.imshow("Camera Source",camera_source_img)
        cv2.imshow("Mask",masked_camera_image)
        cv2.imshow("Biggest Object in Mask",cc_masked_camera_image)
        cv2.imshow("Drawing",src_img_gui)


        cv2.moveWindow("Camera Source" ,x = 20,y = 0)
        cv2.moveWindow("Mask" ,x = 20,y = resolution[0])
        cv2.moveWindow("Drawing" ,x = resolution[1]+200 ,y = 0)
        cv2.moveWindow("Biggest Object in Mask" ,x = resolution[1]+200 ,y = resolution[0])


        #* ---Behavior of keyboard interrupts---
        pressed_key = cv2.waitKey(1) & 0xFF # To prevent NumLock issue
        if pressed_key  == ord('q'): 
            print("Quitting program")
            exit()
            

    





    #-----------------------------
    # Termination
    #-----------------------------








if __name__ == "__main__":
    main()

