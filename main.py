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

#-----------
# Functions
#-----------

def biggestBlob(masked_image):
#* Receives the unfiltered masked image and returns the mask with the biggest blob and it's centroid

    connectivity = 8 # Whether to check for the diagonal pixels or not, should be 4 if not considering diagonals
        
    # cv2.CV_8U stands for images with unsigned chars, which matchs the programm's needs
    cc_output_matrix = cv2.connectedComponentsWithStats(masked_image,connectivity,cv2.CV_8U)
    
    cc_num_lables = cc_output_matrix[0]
    cc_labels = cc_output_matrix[1] 
    cc_stats = cc_output_matrix[2]
    cc_centroids = cc_output_matrix[3]

    print(cc_stats[1:cc_num_lables,4]) # Array de sizes dos elementos
    # TODO Extrair o numero da linha q corresponde à label do maior elemento



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

    #* ---Creating a blank image to drawn on---
    src_img = np.zeros([720, 1280, 3],dtype = np.uint8)
    src_img[:] = 255

    src_img_gui = deepcopy(src_img)

    #-----------------------------
    # Processing
    #-----------------------------

    #* ---Creating boundary arrays for masking---
    upper_bound_bgr = np.array([color_boundaries['limits']['B']['max'], color_boundaries['limits']['G']['max'], color_boundaries['limits']['R']['max']] )
    lower_bound_bgr = np.array([color_boundaries['limits']['B']['min'], color_boundaries['limits']['G']['min'], color_boundaries['limits']['R']['min']] )



    #-----------------------------
    # Visualization
    #-----------------------------

    #* ---Creating windows---
    cv2.namedWindow("Camera Source",cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Mask",cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Biggest Object in Mask",cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Drawing")

    #* ---Configuring mouseCallback---
    

    while(1):

        #* ---Camera source image processing---
        _,camera_source_img = capture_object.read()
        camera_source_img = cv2.flip(camera_source_img,1) # Flip image on x-axis


        #* ---Masked image processing---
        masked_camera_image = cv2.inRange(camera_source_img,lower_bound_bgr,upper_bound_bgr) # Matrix of 0's and 255's

        #* ---Filtering the biggest blob in the image---
        #TODO need to update inputs

        biggestBlob(masked_camera_image)
       


        
    


        #* ---Image showing---
        cv2.imshow("Camera Source",camera_source_img)
        cv2.imshow("Mask",masked_camera_image)

        #* ---Behavior of keyboard interrupts---
        pressed_key = cv2.waitKey(0) & 0xFF # To prevent NumLock issue
        if pressed_key  == ord('q'): 
            print("Quitting program")
            exit()
            

    





    #-----------------------------
    # Termination
    #-----------------------------








if __name__ == "__main__":
    main()

