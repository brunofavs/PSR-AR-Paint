import cv2
from math import sqrt

#! ------------------------ ADD COMMENTS TO THE FINAL VERSION ------------------------

def drawRectangle(img2draw, points, options, shape_points, flip_flop,puzzle_mode,puzzle):
 
    flip_flop['c_counter'] = 0
    flip_flop['e_counter'] = 0

    if len(points['x'])<2 :
        return

    if puzzle_mode:
        copy = puzzle.copy()
    else:
        copy = img2draw.copy()



    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    
    cv2.rectangle(copy, shape_points['ipoints'], shape_points['fpoints'], options['color'], options['size'])
    
    #! Don't even know how this works, showing 2 pics at the same window followed one by the other
    if puzzle_mode:
        cv2.imshow('Puzzle', copy)
    else:
        cv2.imshow('Drawing', copy)

    
    if flip_flop['r_counter'] == 2:
        cv2.rectangle(img2draw, shape_points['ipoints'], shape_points['fpoints'], options['color'], options['size'])
        flip_flop['r_counter'] = 0


def drawCircle(img2draw, points, options, shape_points, flip_flop,puzzle_mode,puzzle):
    
    flip_flop['r_counter'] = 0
    flip_flop['e_counter'] = 0

    if len(points['x'])<2 :
        return

    if puzzle_mode:
        copy = puzzle.copy()
    else:
        copy = img2draw.copy()


    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    radius = int(sqrt(((shape_points['ipoints'][0]-shape_points['fpoints'][0])**2)+((shape_points['ipoints'][1]-shape_points['fpoints'][1])**2)))

    cv2.circle(copy, shape_points['ipoints'], radius, options['color'], options['size'])

    if puzzle_mode:
        cv2.imshow('Puzzle', copy)
    else:
        cv2.imshow('Drawing', copy)


    if flip_flop['c_counter'] == 2:
        cv2.circle(img2draw, shape_points['ipoints'], radius, options['color'], options['size'])
        flip_flop['c_counter'] = 0


def drawEllipse(img2draw, points, options, shape_points, flip_flop,puzzle_mode,puzzle):
    
    flip_flop['c_counter'] = 0
    flip_flop['r_counter'] = 0

    if len(points['x'])<2 :
        return

    if puzzle_mode:
        copy = puzzle.copy()
    else:
        copy = img2draw.copy()

    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    center_point = abs((shape_points['fpoints'][0]+shape_points['ipoints'][0])//2), abs((shape_points['fpoints'][1]+shape_points['ipoints'][1])//2)
    axes = abs((shape_points['fpoints'][0]-shape_points['ipoints'][0])//2), abs((shape_points['fpoints'][1]-shape_points['ipoints'][1])//2)
    
    cv2.ellipse(copy, center_point, axes, 0, 0, 360, options['color'], options['size'])

    if puzzle_mode:
        cv2.imshow('Puzzle', copy)
    else:
        cv2.imshow('Drawing', copy)
    
    if flip_flop['e_counter'] == 2:
        cv2.ellipse(img2draw, center_point, axes, 0, 0, 360, options['color'], options['size'])
        flip_flop['e_counter'] = 0
