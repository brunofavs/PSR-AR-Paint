#!/usr/bin/env python3
import argparse
import cv2
import numpy as np
from functools import partial
import json


# Can't use a dictionary on onTrackbar since I can't assing default values to a input dictionary.

def onTrackbar(x , dict ,red_min = False,red_max = False,green_min = False,green_max = False, blue_min = False,blue_max = False):
    # ------ BLUE ----
    if blue_min == True:
        dict['limits']['B']['min'] = x

    if blue_max == True:
        dict['limits']['B']['max'] = x

    #------ GREEN ----
    if green_min == True:
        dict['limits']['G']['min'] = x

    if green_max == True:
        dict['limits']['G']['max'] = x

    #------ Red ----
    if red_min == True:
        dict['limits']['R']['min'] = x

    if red_max == True:
        dict['limits']['R']['max'] = x

def main():
#-----------------------------
# Initialization
#-----------------------------
    parser = argparse.ArgumentParser(description='Video color segmenting') 

    #Inicial values just to show the image inicially
    # limitsDict ={'limits' : { 'B':{ 'max' : 100 , 'min' : 70 },
    #                           'G':{ 'max' : 120 , 'min' : 90 },
    #                           'R':{ 'max' : 150 , 'min' : 100 } } }

    json_object = open("limits.json")

    limitsDict = json.load(json_object)

    upper_bound_bgr = np.array([limitsDict['limits']['B']['max'], limitsDict['limits']['G']['max'], limitsDict['limits']['R']['max']] )
    lower_bound_bgr = np.array([limitsDict['limits']['B']['min'], limitsDict['limits']['G']['min'], limitsDict['limits']['R']['min']] )


    capture_object = cv2.VideoCapture(0)
    # capture_object.set(cv2.CAP_PROP_EXPOSURE, 0) My camera doesn't support this feature
    #-----------------------------
    # Processing
    #-----------------------------
   
    
    _,source_image_bgr = capture_object.read()
    image_mask_bgr = cv2.inRange(source_image_bgr, lower_bound_bgr, upper_bound_bgr)
  

    #-----------------------------
    # Visualization
    #-----------------------------
    cv2.namedWindow("Source",cv2.WINDOW_AUTOSIZE);
    cv2.imshow("Source",source_image_bgr)


    cv2.namedWindow("Segmentation",cv2.WINDOW_AUTOSIZE);
    cv2.imshow("Segmentation",image_mask_bgr)


    cv2.createTrackbar("Blue_Min","Segmentation",limitsDict['limits']['B']['min'],255,partial(onTrackbar, blue_min = True, dict = limitsDict))
    cv2.createTrackbar("Blue_Max","Segmentation",limitsDict['limits']['B']['max'],255,partial(onTrackbar, blue_max = True, dict = limitsDict) )

    cv2.createTrackbar("Green_Min","Segmentation",limitsDict['limits']['G']['min'],255,partial(onTrackbar, green_min = True, dict = limitsDict) )
    cv2.createTrackbar("Green_Max","Segmentation",limitsDict['limits']['G']['max'],255,partial(onTrackbar, green_max = True, dict = limitsDict) )

    cv2.createTrackbar("Red_Min","Segmentation",limitsDict['limits']['R']['min'],255,partial(onTrackbar, red_min = True, dict = limitsDict) )
    cv2.createTrackbar("Red_Max","Segmentation",limitsDict['limits']['R']['max'],255,partial(onTrackbar, red_max = True, dict = limitsDict) )

    while(1):

        _,source_image_bgr = capture_object.read()
        source_image_bgr = cv2.flip(source_image_bgr,1)
        
        
        cv2.imshow('Source',source_image_bgr)

        # Since list assigns as copies, we need to update the bounds
        upper_bound_bgr = np.array([limitsDict['limits']['B']['max'], limitsDict['limits']['G']['max'], limitsDict['limits']['R']['max']] )
        lower_bound_bgr = np.array([limitsDict['limits']['B']['min'], limitsDict['limits']['G']['min'], limitsDict['limits']['R']['min']] )


        image_mask = cv2.inRange(source_image_bgr, lower_bound_bgr, upper_bound_bgr)
        cv2.imshow('Segmentation',image_mask)

        pressed_key = cv2.waitKey(1) & 0xFF

        if pressed_key  == ord('w'): #NUMLOCK ISSUE ms delay
            file_name = 'limits.json'
            with open(file_name, 'w') as file_handle:
                print('Writing dictionary limits to file ' + file_name)
                json.dump(limitsDict, file_handle)

        elif pressed_key == ord('q'): 
            print("Quiting program.")
            exit(0)
    

    #-----------------------------
    # Termination
    #-----------------------------
    
    
if __name__=="__main__":
    main()

