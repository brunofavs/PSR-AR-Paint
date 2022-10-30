import argparse
from cmath import sqrt
import cv2
import numpy as np
import json
import pprint
import time
import pick




# x,y = cc_centroids[max_label]

# centroid = centroid_tuple(x= int(x),y=int(y)) 





def drawingLine(white_board,points,options,usp):

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

    #* ---Checking whether distance is good if ups----
    if usp: 
        distance = sqrt((inicial_point[0]-final_point[0])**2+(inicial_point[1]-final_point[1])**2)
        if distance > 100:
           return

    #Python passes arguments by assignment, since a np array is mutable, we're just
    #modifying the inicial image, not changing the original memory adress
    cv2.line(white_board, inicial_point, final_point, options['color'], options['size'])
    
    return white_board


