# #!/usr/bin/env python3

import cv2
from math import sqrt


def drawRectangle(whiteboard, points, options, shape_points, flip_flop):
    ix, iy = shape_points['ipoints']
    copy = whiteboard.copy()
    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    cv2.rectangle(copy, (ix, iy), shape_points['fpoints'], options['color'], options['size'])
    cv2.imshow('Drawing', copy)
    if flip_flop['r_counter'] == 2:
        cv2.rectangle(whiteboard, (ix, iy), shape_points['fpoints'], options['color'], options['size'])
        flip_flop['r_counter'] = 0

def drawCircle(whiteboard, points, options, shape_points):
    copy = whiteboard.copy()
    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    radius = int(sqrt(((shape_points['ipoints'][0]-shape_points['fpoints'][0])**2)+((shape_points['ipoints'][1]-shape_points['fpoints'][1])**2)))
    cv2.circle(copy, shape_points['ipoints'], radius, options['color'], options['size'])
    cv2.imshow('Drawing', copy)

def drawEllipse(whiteboard, points, options, shape_points):
    copy = whiteboard.copy()
    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    axes = (abs(shape_points['ipoints'][0]-shape_points['fpoints'][0]), abs(shape_points['ipoints'][1]-shape_points['fpoints'][1]))

    #cv2.ellipse(whiteboard, shape_points['ipoints'], axes, angle, options['color'], options['size'])