from fastcam import Stream

import cv2
import numpy as np
camera = 0
#calibration
points = []

def click(event, x, y, flags, param):

    
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) == 3:
            print('You have defined enough points!')
        else:
            points.append((x,y))
            print('points : ' + str(points))

cv2.namedWindow('calibration')
cv2.setMouseCallback('calibration', click)


cap = cv2.VideoCapture(camera)

width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

print(width)
print(height)

if not cap.isOpened:
    print('cap didn\'t open')
while True:
    ok , frame = cap.read()
    for point in points:
        cv2.circle(frame, point, 10, (255,0,0),5, cv2.FILLED, shift=0)
        
    cv2.imshow('calibration', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    if len(points) == 3:
        break
cv2.destroyAllWindows()
cap.release()

srcTri = np.array(points ).astype(np.float32)
dstTri = np.array( [[0,0],[width,0], [0,height]] ).astype(np.float32)
warp_mat = cv2.getAffineTransform(srcTri, dstTri)

stream = Stream(camera)
stream.start(5)
while True:

    frame = stream.read()
    frame = cv2.warpAffine(frame,warp_mat, ( int(width) , int(height)))
    frame = cv2.putText(frame, 'queue len: '+ str(stream.current_size), (50,50), cv2.FONT_HERSHEY_SIMPLEX,  1, (0,0,255), 2, cv2.LINE_AA)
    cv2.imshow('webcam', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        stream.stop()
        break

cv2.destroyAllWindows()

