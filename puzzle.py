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

    puzzle_3D = np.ones([res[0], res[1],3],dtype = np.uint8)*255

    border_points = fullLinePoints(res,wanted_lines)

    for i in range(0,len(border_points),2):
        cv2.line(puzzle_3D, tuple(border_points[i]), tuple(border_points[i+1]), (0,0,0), 3)

    cv2.imshow('te',puzzle_3D)
    cv2.waitKey(0)

    return

# puzzle_3D = buildPuzzle((400,600),4)

def puzzle_zones(puzzle_BGR):
    #* This function will yield a dictionary with the masks corresponding to each color, the position of the centroids on which we will draw
    #* the color letter, and the zone_dicts will dictate which label zone is which color
    def splitList(alist, wanted_parts=1):
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
                                                for i in range(wanted_parts) ]

    pass
