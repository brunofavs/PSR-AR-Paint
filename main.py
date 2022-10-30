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
from multiprocessing.connection import wait
import cv2
import numpy as np
import json
import pprint
import time
import pick

import puzzle
import shapes

from functools import partial
from copy import deepcopy
from collections import namedtuple


#-----------
# Global variables
#-----------

centroid_tuple = namedtuple('centroid_tuple',['x','y']) # No point in being a dictionary as I dont ever want to change the coordinates of the centroid
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

        centroid = centroid_tuple(x= -50,y=-50) 

        return empty_mask,centroid; 
    else :
        max_label = cc_areas.argmax() + 1 # +1 because we're ignoring idx 0, bcs its background

    #* ---Calculates the mask with the biggest blob----

    cc_mask = np.zeros([resolution[0], resolution[1]],dtype = np.uint8) # Matrix of 0's 480x640

    cc_mask[cc_labels==max_label] = cc_labels[cc_labels==max_label] # Matrix with 0's and max label's number

    # cc_mask_bool = cc_mask.astype(bool) # Matrix with 0's and 1's


    #* ---Calculates the centroid of the biggest blob----

    x,y = cc_centroids[max_label]
    centroid = centroid_tuple(x= int(x),y=int(y)) # Need casting because the image matrix is uint8

    
    return cc_mask,centroid

def drawingLine(white_board,points,options):

    if points['x'][-1] == -50 :
        points['x'].pop(-1)
        points['y'].pop(-1)

    # If it pops, then it returns and doesnt draw anything, this prevents big lines across to (-50,-50)

    #* ---Checking whether there are enough points to draw a line----
    if len(points['x']) < 2: 
        return
    #It only reaches here if there are enough points to draw a line

    #* ---Drawing the line in the input image----
    inicial_point = (points['x'][-2],points['y'][-2] )
    final_point = (points['x'][-1],points['y'][-1] )
    
    #Python passes arguments by assignment, since a np array is mutable, we're just
    #modifying the inicial image, not changing the original memory adress
    cv2.line(white_board, inicial_point, final_point, options['color'], options['size'])
    
def keyboardActions(pencil_options,src_img_gui,switcher):
    pressed_key = cv2.waitKey(1) & 0xFF # To prevent NumLock issue
    if pressed_key  == ord('q'): 
        print("Quitting program")
        exit()
    elif pressed_key == ord('r'):
        pencil_options['color'] = (0,0,255)
        print("Changing color to red")

    elif pressed_key == ord('g'):
        pencil_options['color'] = (0,255,0)
        print("Changing color to green")

    elif pressed_key == ord('b'):
        pencil_options['color'] = (255,0,0)
        print("Changing color to blue")
    
    elif pressed_key == ord('+'):
        
        if pencil_options['size'] < 50 :

            pencil_options['size'] += 1
            print("Increasing pencil size to " + str(pencil_options['size']))
        else:
            print("Max pencil size reached (" + str(pencil_options['size']) + ") !"  )

    elif pressed_key == ord('-'):

        if pencil_options['size'] > 1:

            pencil_options['size'] -= 1
            print("Decreasing pencil size to " + str(pencil_options['size']))
        else:
            print("Min pencil size reached (" + str(pencil_options['size']) + ") !"  )

    elif pressed_key == ord('c'):
        src_img_gui[:] = 255 # Resets to inicial value
        print("Clearing whiteboard!")

    elif pressed_key == ord('s'):
        date = time.ctime(time.time())
        file_name = "Drawing " + date +".png"
        print("Saving png image as " + file_name)
        cv2.imwrite(file_name , src_img_gui) #! Caso seja com o video pode ter de se mudar aqui

    elif pressed_key == ord('v'):
        switcher['counter'] = not switcher['counter']
        


    #TODO implementar try except para caso não consiga escrever

def drawingCore(camera_source_img, masked_camera_image,img_gui,centroids,pencil_options):

        #* ---Filtering the biggest blob in the image---

        cc_mask , cc_centroid = biggestBlob(masked_camera_image)
         
        cc_masked_camera_image = np.where(cc_mask,masked_camera_image,0)  


        #* ---Drawing a x where the centroid is in the source---
        # TODO For now will just draw a circle
        cv2.drawMarker(camera_source_img, cc_centroid, (0,0,255), 0, 20, 2)
        #cv2.circle(camera_source_img,cc_centroid,10,(0,0,255),-1)


        #* ---Storing centroids---
        centroids['x'].append(cc_centroid.x) # cc_centroid is a namedTuple
        centroids['y'].append(cc_centroid.y)

        if len(centroids['x']) != len(centroids['y']): # Just for debbuging, may not ever be necessary
            print("Something went wrong, more x's than y's")
            exit()
        
        if len(centroids['x']) >= 3 :
            centroids['x'] = centroids['x'][-2:] # If the list gets too big, cleans it back to the last 2, which are needed for drawing
            centroids['y'] = centroids['y'][-2:] 

        #* ---Drawing---
        drawingLine(img_gui,centroids,pencil_options)
        #* ---Showing biggest object in mask---

        #! This is here because cc_masked_camera_image is only relevant inside this fc and didn't want to have it as output
        cv2.imshow("Biggest Object in Mask",cc_masked_camera_image)

def switchOutput(src_img_gui,camera_source_img,switcher):
   
    mask = cv2.inRange(src_img_gui,(254,254,254),(255,255,255))

    if switcher['counter']:
        camera_source_img[mask==0] = src_img_gui[mask==0]   #! joins the circle and the camera image


#-----------
# Main
#-----------

def main():
    #-----------------------------
    # Initialization
    #-----------------------------

    #* ---Configuration of argparse----
    parser = argparse.ArgumentParser(description='AR paint') 
    parser.add_argument('-j','--json',type=str,required=True,help='Absolute path for json file with color thresholds') 
    parser.add_argument('-usp','--use_shake_prevention', action='store_true',default = False ,help='Use shake mode : Prevents unintended lines across long distances')
    args = parser.parse_args()

    #* ---Configuration of variable for flip flop to use with switchOutput function
    switcher = {'counter': False}

    #* ---Mode selection----

    title_prompt = "Please choose the gamemode : "
    options = ["Normal","Puzzle"]
    option , index = pick.pick(options, title_prompt,indicator="=>")

    puzzle_mode = False
    normal_mode = False

    if index == 0:
        normal_mode = True
    elif index == 1:
        puzzle_mode = True
    else:
        return 

    #* ---Loading json file into memory----
    json_inicial_object = open(args.json)
    color_boundaries = json.load(json_inicial_object)

    #* ---Setting up videoCapture object----
    capture_object = cv2.VideoCapture(0)  #! Camera images will be camera_src_img
    _,camera_source_img = capture_object.read() # Need this to configure resolution

    #* ---Initializing random variables----
    resolution = camera_source_img.shape
    centroids = { 'x' : [], 'y' : []}


    #* ---Creating a blank image to drawn on---
    src_img = np.zeros([resolution[0], resolution[1], 3],dtype = np.uint8)
    src_img[:] = 255

    src_img_gui = deepcopy(src_img)

    #* ---Initializing a options dictionary with size and color---

    pencil_options = {'size' : 10, 'color' : (0,0,255)} # Inicial 10px red

     #* ---Puzzle Initialization---

    # TODO Add difficulty, by increasing number of lines
    
    if puzzle_mode:
         #* ---Calculating a random puzzle matrix---
        src_puzzle = puzzle.buildPuzzle( (resolution[0],resolution[1]), 4)

         #* ---Sum of all puzzle pixels in 1D---
        num_of_puzzle_pixels = src_puzzle[:,:,0].size#Important to not include the black pixels in the total, also not the letters
        #! Important that this is before drawing zone letters
        

         #* ---Calculating puzzle data---
        mask_dict, puzzle_centroids , zone_labels_dict = puzzle.puzzleZones(src_puzzle)

         #* ---Drawing letters on zones---
        puzzle.drawZoneLetters(src_puzzle,puzzle_centroids,zone_labels_dict)

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
    
    if puzzle_mode :
        cv2.namedWindow("Puzzle")
    else:
        cv2.namedWindow("Drawing")


    #* ---Configuring mouseCallback---
    #TODO mouseCallback


    while(1):

        #* ---Camera source image processing---
        _,camera_source_img = capture_object.read()
        camera_source_img = cv2.flip(camera_source_img,1) # Flip image on x-axis

        #* ---Masked image processing---
        masked_camera_image = cv2.inRange(camera_source_img,lower_bound_bgr,upper_bound_bgr) # Matrix of 0's and 255's

        #* ---Drawing Core---
        drawingCore(camera_source_img, masked_camera_image,src_img_gui,centroids,pencil_options)

        #* ---Puzzle processing---
        # TODO Figure how to implement this
       
        if puzzle_mode:
            
            puzzle_painted = np.where(True,src_img_gui,0) # This basically does a copy of src img gui without copying memory adress

            # TODO Figure out why the ***** commenting this fixes blue_only_mask
            # src_img_gui[src_puzzle == (0,0,0)] =  0 # This prevents the borders from entering the calculation of correct pixels

            puzzle_painted[ src_puzzle== (0,0,0) ] = 0  # This draws the puzzle on puzzle_painted

        #* ---Puzzle evaluation---

        if puzzle_mode:
            
            blue_channel  = src_img_gui  [:,:,0]
            green_channel = src_img_gui  [:,:,1]
            red_channel   = src_img_gui  [:,:,2]


            blue_only_mask  = np.logical_and((red_channel == 0) , (green_channel == 0)  , (blue_channel == 255) )
            green_only_mask = np.logical_and((red_channel == 0) , (green_channel == 255), (blue_channel == 0)   )
            red_only_mask   = np.logical_and((red_channel == 255), (green_channel == 0) , (blue_channel == 255) )

            blue_correct_pxs  = sum( sum(np.logical_and(blue_only_mask , mask_dict['blue_mask']  )))
            green_correct_pxs = sum( sum(np.logical_and(green_only_mask, mask_dict['green_mask'] )))
            red_correct_pxs   = sum( sum(np.logical_and(red_only_mask  , mask_dict['red_mask']   )))


            blue_incorrect_pxs  = sum( sum( np.logical_and(blue_only_mask , np.logical_not(mask_dict['blue_mask']  ))))
            green_incorrect_pxs = sum( sum( np.logical_and(green_only_mask, np.logical_not(mask_dict['green_mask'] ))))
            red_incorrect_pxs   = sum( sum( np.logical_and(red_only_mask  , np.logical_not(mask_dict['red_mask']   ))))

            score_numerator = (blue_correct_pxs + green_correct_pxs + red_correct_pxs) - (blue_incorrect_pxs + green_incorrect_pxs + red_incorrect_pxs)
            # print('numertator is',score_numerator)
            # print(num_of_puzzle_pixels)
            score = int((score_numerator/num_of_puzzle_pixels)*100)

            if score < 0:
                score = 0

            print("Your score is ",score," %.")

        #* ---Storing centroids---
        #centroids['x'].append(cc_centroid.x) # cc_centroid is a namedTuple
        #centroids['y'].append(cc_centroid.y)

        #* ---Behavior of keyboard interrupts---

        keyboardActions(pencil_options,src_img_gui,switcher)

        #-----------------------------
        # Visualization
        #-----------------------------


        #* ---Switch the drawing background from whiteboard to camera and vise-versa---

        switchOutput(src_img_gui,camera_source_img,switcher)

        #* ---Drawing shapes---

        #shapes.drawCircle(src_img_gui, centroids, options)

        #* ---Image showing---
        
        #// cv2.imshow("Biggest Object in Mask",cc_masked_camera_image) on drawingCore
        cv2.imshow("Camera Source",camera_source_img)
        cv2.imshow("Mask",masked_camera_image)
        

        if puzzle_mode :
            cv2.imshow("Puzzle",puzzle_painted)
        else:
            cv2.imshow("Drawing",src_img_gui)
                
        
        cv2.moveWindow("Camera Source" ,x = 20,y = 0)
        cv2.moveWindow("Mask" ,x = 20,y = resolution[0])
        cv2.moveWindow("Biggest Object in Mask" ,x = resolution[1]+200 ,y = resolution[0])
        
        if puzzle_mode:
            cv2.moveWindow("Puzzle" ,x = resolution[1]+200 ,y = 0)
        else:
            cv2.moveWindow("Drawing" ,x = resolution[1]+200 ,y = 0)

        
        
            
    #-----------------------------
    # Termination
    #-----------------------------








if __name__ == "__main__":
    main()

        # TODO Clean this once debugged

            # red_only_mask = red_only_mask.astype(np.uint8)  #convert to an unsigned byte
            # red_only_mask*=255

            # green_only_mask = green_only_mask.astype(np.uint8)  #convert to an unsigned byte
            # green_only_mask*=255

            # blue_only_mask = blue_only_mask.astype(np.uint8)  #convert to an unsigned byte
            # blue_only_mask*=255

            # cv2.imshow('red',red_only_mask)
            # cv2.imshow('green',green_only_mask)
            # cv2.imshow('blue',blue_only_mask)


            # # cv2.imshow('blue channel',blue_channel)
            # # cv2.imshow('green channel',green_channel)
            # # cv2.imshow('red channel',red_channel)
