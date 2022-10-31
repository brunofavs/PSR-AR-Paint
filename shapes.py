# #!/usr/bin/env python3

import cv2

def drawRectangle(whiteboard, points, options, shape_points):

    shape_points['fpoints'] = (points['x'][-2],points['y'][-2] )
    copy = whiteboard.copy()
    cv2.rectangle(copy, shape_points['ipoints'], shape_points['fpoints'], options['color'], options['size'])
    cv2.imshow('Drawing', copy)