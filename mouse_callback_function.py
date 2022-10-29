import numpy as np
import cv2 




run = False
def draw(event, x, y, flag, param):
    global run
    if event == cv2.EVENT_LBUTTONDOWN:
        run = True
        cv2.circle(win, (x,y), 2, (0,255,0), 2)
    if event == cv2.EVENT_LBUTTONUP:
        run = False

    if event == cv2.EVENT_MOUSEMOVE:
        if run == True:
            cv2.circle(win, (x,y), 2, (0,255,0), 2)




cv2.namedWindow("window")
cv2.setMouseCallback("window", draw)


win = np.zeros((500,500,3), dtype= 'float64')

while True:

    cv2.imshow("window", win)
    k = cv2.waitKey(1)

    if k == 27:
        cv2.destroyAllWindows()
        break