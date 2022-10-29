#!/usr/bin/env python3

# function must have centroid coords as an input
# 's' key for squares, 'e' key for ellipses and 'o' key for circles
# for the cirle, when the 'o' key is pressed the centroid position is the circle origin
# in the ellipse case,

import cv2
from math import sqrt


def drawCircle(white_board, points, options):

    center_point = (points['x'][-2], points['y'][-2])
    final_point = (points['x'][-1], points['y'][-1])
    cx, cy = center_point[0], center_point[1]
    rx, ry = final_point[0], final_point[1]
    radius = int(sqrt(((cx-rx)**2)+((cy-ry)**2)))

    #white_board_copy = white_board.copy()

    cv2.circle(white_board, center_point, radius, options['color'], options['size'])


def drawSquares(white_board, points, options):
    if points['x'][-1] == -50 :
        points['x'].pop(-1)
        points['y'].pop(-1)

    if len(points['x']) < 2: 
        return

    center_point = (points['x'][-2], points['y'][-2])
    final_point = (points['x'][-1], points['y'][-1])

    cv2.rectangle(white_board, center_point, final_point, options['color'], options['size'])


def drawEllipse():
    pass
