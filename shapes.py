# #!/usr/bin/env python3

# import cv2
# from math import sqrt
# from pynput import keyboard

# coords={'ix':-1,'iy':-1,'x':-1,'y':-1}

# def drawCircle(white_board, points, options):
    
#     def on_press(key):
#         if 'char' in dir(key) and key.char == 'p':
#             coords['ix'],coords['iy'] = points['x'][-2],points['y'][-2]
#             print(coords['ix'],coords['iy'])

#     def on_release(key):
#         if 'char' in dir(key) and key.char == 'p':
#             coords['x'],coords['y'] = points['x'][-2],points['y'][-2]
#             radius = int(sqrt(((coords['ix'] - coords['x'])**2)+((coords['iy'] - coords['y'])**2)))
#             cv2.circle(white_board, (coords['ix'], coords('iy')), radius, options['color'], options['size'])
#             cv2.imshow('Drawing', white_board)
#     # Collect events until released
#     with keyboard.Listener(
#             on_press=on_press,
#             on_release=on_release) as listener:
#         listener.join()


# def drawSquare(white_board, points, options):
#     pass

# def drawEllipse():
#     pass
