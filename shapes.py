import cv2
from math import sqrt


def drawRectangle(whiteboard, points, options, shape_points, flip_flop):
    copy = whiteboard.copy()

    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    
    cv2.rectangle(copy, shape_points['ipoints'], shape_points['fpoints'], options['color'], options['size'])
    cv2.imshow('Drawing', copy)
    
    if flip_flop['r_counter'] == 2:
        cv2.rectangle(whiteboard, shape_points['ipoints'], shape_points['fpoints'], options['color'], options['size'])
        flip_flop['r_counter'] = 0

def drawCircle(whiteboard, points, options, shape_points, flip_flop):
    copy = whiteboard.copy()

    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    radius = int(sqrt(((shape_points['ipoints'][0]-shape_points['fpoints'][0])**2)+((shape_points['ipoints'][1]-shape_points['fpoints'][1])**2)))

    cv2.circle(copy, shape_points['ipoints'], radius, options['color'], options['size'])
    cv2.imshow('Drawing', copy)

    if flip_flop['c_counter'] == 2:
        cv2.circle(whiteboard, shape_points['ipoints'], radius, options['color'], options['size'])
        flip_flop['c_counter'] = 0

def drawEllipse(whiteboard, points, options, shape_points, flip_flop):
    copy = whiteboard.copy()

    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    center_point = abs((shape_points['fpoints'][0]+shape_points['ipoints'][0])//2), abs((shape_points['fpoints'][1]+shape_points['ipoints'][1])//2)
    axes = abs((shape_points['fpoints'][0]-shape_points['ipoints'][0])//2), abs((shape_points['fpoints'][1]-shape_points['ipoints'][1])//2)
    
    cv2.ellipse(copy, center_point, axes, 0, 0, 360, options['color'], options['size'])
    cv2.imshow('Drawing', copy)

    if flip_flop['e_counter'] == 2:
        cv2.ellipse(whiteboard, center_point, axes, 0, 0, 360, options['color'], options['size'])
        flip_flop['e_counter'] = 0



