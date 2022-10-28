#!/usr/bin/env python3

# -----------
# Conventions
# -----------

# ! camelCase for functions and methods
# ! snake_case for variables

# -----------
# Imports
# -----------
import argparse
import cv2
import numpy as np
from functools import partial
import json
from copy import deepcopy
import random
# -----------
# Functions
# -----------

def buildPuzzle(res,wanted_lines):

    def fullLinePoints(res,wanted_lines):
        #* Generates random points and returns the points on the border by linear interpolation

        #* Generates random points list by using nested list comprehension
        points =[ ( [random.randint(0,res[i]) for i in range(0,2)] ) for _ in range(0,wanted_lines*2) ]

        #* Interpolation of points to the borders
        border_points = []

        for i in range(0,len(points),2):
            # a and b are both inicial points, p and q are border points px = 0, qx = img.width
            ax = points[i][0]
            ay = points[i][1]
            bx = points[i+1][0]
            by = points[i+1][1]

            #* Checking if there are perfectly vertical lines, which break the algorithm
            if ax == bx :
                ax += 1

            #* Calculating border points based on slope
            slope = (ay-by)/(ax-bx) # Non integer division
            py = ay - ax * slope
            qy = by + (res[1]-bx)*slope

            border_points.append([0,int(py)])
            border_points.append([res[1],int(qy)])

        return border_points

    #* Creating a blank image
    puzzle_3D = np.ones([res[0], res[1],3],dtype = np.uint8)*255

    #* Calculatins border points to draw lines
    border_points = fullLinePoints(res,wanted_lines)

    #* Drawing the lines
    for i in range(0,len(border_points),2):
        cv2.line(puzzle_3D, tuple(border_points[i]), tuple(border_points[i+1]), (0,0,0), 3)

    #TODO Decide whether this blur is worth staying
    puzzle_3D = cv2.GaussianBlur(puzzle_3D,(3,3),cv2.BORDER_DEFAULT)

    return puzzle_3D

def puzzleZones(puzzle_BGR):


    #* This function will yield a dictionary with the masks corresponding to each color, the position of the centroids on which we will draw
    #* the color letter, and the zone_dicts will dictate which label zone is which color

    def splitList(alist, wanted_parts=1):
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
                                                for i in range(wanted_parts) ]

    def buildMask(cc_labels,label_color_list,res):

        buffer_list = []
        for i in range(len(label_color_list)):
            buffer_list.append(np.where(cc_labels == label_color_list[i],255,0))

        mask_int64 = np.zeros( [res[0], res[1]] ,dtype = np.int64) #! Needs to be int64 so that it can add because cc_labels is int64
        for img in buffer_list:
            mask_int64 += img

        mask_uint8 = mask_int64.astype(np.uint8)  

        return mask_uint8

    res = puzzle_BGR.shape
    #* Converting BGR to Gray
    puzzle_gray = cv2.cvtColor(puzzle_BGR,cv2.COLOR_BGR2GRAY)

    #* Converting Gray to Binnary
    # Redudant step, as the gray image already is 0's and 255's
    _,puzzle_1D = cv2.threshold(puzzle_gray,128,255,cv2.THRESH_BINARY)
    
    #* Calculating puzzle areas
    connectivity = 8 # Whether to check for the diagonal pixels or not, should be 4 if not considering diagonals
        
    # cv2.CV_8U stands for images with unsigned chars, which matchs the programm's needs
    cc_output_matrix = cv2.connectedComponentsWithStats(puzzle_1D,connectivity,cv2.CV_8U)

    cc_num_lables = cc_output_matrix[0]
    cc_labels = cc_output_matrix[1] 
    cc_stats = cc_output_matrix[2]  # May not be needed, anyway its there.
    cc_centroids = cc_output_matrix[3]

    cc_centroids = cc_centroids.astype(int)

    #* Assigning labels randomly to r,g,b

    label_list = list(range(1,cc_num_lables))
    random.shuffle(label_list)
    
    reds,greens,blues = splitList(label_list,3) # Each list contains which label corresponds to each color, in case of mod(len(label_list),3) != 0, the blues will have always 1 more

    zones_labels_dict = {'blues':blues, 'greens':greens, 'reds': reds}

    #* Building the masks of 0 and 255
    red_mask = buildMask(cc_labels,reds,res)
    green_mask = buildMask(cc_labels,greens,res)
    blue_mask = buildMask(cc_labels,blues,res)
   
    mask_dict = {'red_mask':red_mask,'green_mask':green_mask,'blue_mask':blue_mask }


    return mask_dict, cc_centroids, zones_labels_dict

def drawZoneLetters(img,centroids,zone_labels_dict):
    # print(zone_labels_dict)
    # print(centroids)
    x_corr = -8
    y_corr = 8

    for i in zone_labels_dict['reds']:
        cv2.putText(img,'R',(puzzle_centroids[i,0]+x_corr,puzzle_centroids[i,1]+y_corr),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),2)

    for i in zone_labels_dict['greens']:
        cv2.putText(img,'G',(puzzle_centroids[i,0]+x_corr,puzzle_centroids[i,1]+y_corr),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),2)

    for i in zone_labels_dict['blues']:
        cv2.putText(img,'B',(puzzle_centroids[i,0]+x_corr,puzzle_centroids[i,1]+y_corr),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),2)

# -----------
# Function testing
# -----------
puzzle_3D = buildPuzzle((400,600),4)

mask_dict, puzzle_centroids , zone_labels_dict = puzzleZones(puzzle_3D)

drawZoneLetters(puzzle_3D,puzzle_centroids,zone_labels_dict)



#! Centroid 0 seems to always be off

cv2.imshow('2fe',puzzle_3D)
cv2.imshow('redmask',mask_dict['red_mask'])
cv2.imshow('greenmask',mask_dict['green_mask'])
cv2.imshow('bluemask',mask_dict['blue_mask'])
cv2.waitKey(0)

