import argparse
import cv2
import numpy as np
from functools import partial
import json


limitsDict ={'limits' : { 'B':{ 'max' : 100 , 'min' : 70 },
                          'G':{ 'max' : 120 , 'min' : 90 },
                          'R':{ 'max' : 150 , 'min' : 100 } } }

upper_bound_bgr = np.array([limitsDict['limits']['B']['max'], limitsDict['limits']['G']['max'], limitsDict['limits']['R']['max']] )  
upper_list = [limitsDict['limits']['B']['max'], limitsDict['limits']['G']['max'], limitsDict['limits']['R']['max'] ]

print(upper_bound_bgr)

limitsDict['limits']['B']['max'] = 199
upper_bound_bgr[0] = limitsDict['limits']['B']['max']

print(upper_bound_bgr)


# print(upper_list)








