import argparse
from cmath import sqrt
import cv2
import numpy as np
import json
import pprint
import time
import pick




x,y = cc_centroids[max_label]

centroid = centroid_tuple(x= int(x),y=int(y)) 

Lx, Ly = cc_centroids['last_x'], cc_centroids['last_y']




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

    if Lx !=-1 and Ly !=-1:
        if usp: #chamar aqui a funçao do argparse
            distance = sqrt((Lx-x)**2+(Ly-y)**2)
            if distance > 100:
                Lx = inicial_point
                Ly = final_point
        cv2.line(white_board, inicial_point, final_point, options['color'], options['size'])
    
    return white_board


