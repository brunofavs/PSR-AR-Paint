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

#-----------------------------
# mousecall to get color 
#-----------------------------
def mouse_BGR(event, x, y, flags, params,source_image):
    if event == cv2.EVENT_LBUTTONDOWN:

        colorsB = source_image[y,x,0]
        colorsG = source_image[y,x,1]
        colorsR = source_image[y,x,2]
        color =  [colorsB,colorsG,colorsR]

        #-----------------------------
        # Blue
        #-----------------------------
        try:
            cv2.setTrackbarPos("Blue_Min","Segmentation",color[0]-15)
        except:
            cv2.setTrackbarPos("Blue_Min","Segmentation",0)

        try:        
            cv2.setTrackbarPos("Blue_Max","Segmentation",color[0]+15)
        except:
            cv2.setTrackbarPos("Blue_Max","Segmentation",255)
            
        #-----------------------------
        # Green
        #-----------------------------
        try:
            cv2.setTrackbarPos("Green_Min","Segmentation",color[1]-15)
        except:
            cv2.setTrackbarPos("Green_Min","Segmentation",0)

        try:        
            cv2.setTrackbarPos("Green_Max","Segmentation",color[1]+15)
        except:
            cv2.setTrackbarPos("Green_Max","Segmentation",255)

        #-----------------------------
        # Red
        #-----------------------------
        try:
            cv2.setTrackbarPos("Red_Min","Segmentation",color[2]-15)
        except:
            cv2.setTrackbarPos("Red_Min","Segmentation",0)

        try:        
            cv2.setTrackbarPos("Red_Max","Segmentation",color[2]+15)
        except:
            cv2.setTrackbarPos("Red_Max","Segmentation",255)


            

        print("BGR Format: ", color)
        print("coordinate of pixel: X: ",x, "Y: ",y)

def main():
#-----------------------------
# Initialization
#-----------------------------
    parser = argparse.ArgumentParser(description='Video color segmenting') 
    parser.add_argument('-j','--json',type=str,required=True,help='Absolute path for json file with color thresholds') 
    args = parser.parse_args()

    try:
        json_object = open(args.json)
        limitsDict = json.load(json_object)
    except:
        print("No json file found to read, starting calibration with default values")
        limitsDict ={'limits' : { 'B':{ 'max' : 100 , 'min' : 70 },
                                  'G':{ 'max' : 120 , 'min' : 90 },
                                  'R':{ 'max' : 150 , 'min' : 100 } } }
    else:
        print("Json file read successfuly, reading starting values for calibration")


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
    cv2.moveWindow('Segmentation', source_image_bgr.shape[1] + 90, 0 )
    
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
        
        cv2.setMouseCallback("Source", partial(mouse_BGR, source_image = source_image_bgr))
        
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
    


    cv2.namedWindow("Source",cv2.WINDOW_AUTOSIZE);
    cv2.imshow("Source",source_image_bgr)

    #cv2.namedWindow('mouseBGR')

    #cv2.imshow('mouseBGR', source_image_bgr_flipped)

    

    while(True):

        _, source_image_bgr = capture_object.read()

        cv2.imshow('mouseRGB', source_image_bgr)

        if cv2.waitKey(1) == 27:
            break

    capture_object.release()
    cv2.destroyAllWindows()



   
    #-----------------------------
    # Termination
    #-----------------------------
    
    
if __name__=="__main__":
    main()

