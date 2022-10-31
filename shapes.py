# #!/usr/bin/env python3

import cv2

def drawRectangle(whiteboard, points, coords, options, flip_flop):
    
    coords['fpoints'] = (points['x'][-2],points['y'][-2] )

    if flip_flop['r_counter'] == 1:
        coords['ipoints'] = (points['x'][-2],points['y'][-2] )
        print(coords['ipoints'])
        cv2.rectangle(whiteboard,coords['ipoints'], coords['fpoints'], options['color'], options['size'])
        flip_flop['r_counter'] += 1

    elif flip_flop['r_counter'] == 3:
        print(coords['fpoints'])
        cv2.rectangle(whiteboard,coords['ipoints'], coords['fpoints'], options['color'], options['size'])
        flip_flop['r_counter'] = 0
