import cv2
import sys
import numpy as np
import argparse
import math
from fastcam import Stream



#choose your input source
camera = '/dev/video0'
queue_length = 5

parser = argparse.ArgumentParser(description = 'magic webcam ;) ')
parser.add_argument('--pipe',dest = 'pipe',help = 'write the results in stdout: on|off (default: off)', choices = ['on','off'], default = 'off')
args = parser.parse_args()
pipe = (args.pipe == 'on')

cap = cv2.VideoCapture(camera)
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
points = []

def click(event, x, y, flags, param):

    
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) == 4:
            print('You have defined enough points!')
        else:
            points.append((x,y))
            print('points : ' + str(points))

            
cv2.namedWindow('calibration')
cv2.setMouseCallback('calibration', click)
while True:
    ok , frame = cap.read()

    for point in points:
        cv2.circle(frame, point, 10, (255,0,0),5, cv2.FILLED, shift=0)
        
    cv2.imshow('calibration', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    if len(points) == 4:
        break
cv2.destroyAllWindows()
cap.release()

srcTri = np.array(points ).astype(np.float32)
#dstTri = np.array( [[0,0],[width,0], [0,height]] ).astype(np.float32)
dstTri = np.array( [[0,0],[1050,0], [0,1500], [1050, 1500]]).astype(np.float32)
#warp_mat = cv2.getAffineTransform(srcTri, dstTri)
warp_mat = cv2.getPerspectiveTransform(srcTri, dstTri)

stream = Stream(camera)
stream.start(queue_length)
'''
w_scale = 300
h_scale = 400

new_w = cv2.transform(points[1], warp_mat)[1] - cv2.transform(points[0], warp_mat)[1]
new_h = cv2.transform(points[2], warp_mat)[0] - cv2.transform(points[0], warp_mat)[0]
'''
mode = None
display_help = True

bilateral_size = 5
bilateral_sigma_color = 0.1
bilateral_sigma_space = 20
while True:

    
    frame = stream.read()
    
    if not ok:
        break
    """
    frame = cv2.warpAffine(frame,warp_mat, (int(w_scale * math.sqrt(( (points[0][0] - points[1][0]) **2 + (points[0][1] - points[1][1])**2 ))) ,
                           int(h_scale *math.sqrt(( (points[0][0] - points[2][0]) **2 + (points[0][1] - points[2][1])**2 )))) )
    """

    #frame = cv2.warpAffine(frame, warp_mat, (1050, 1500))
    frame = cv2.warpPerspective(frame, warp_mat, (1050, 1050))
    
    '''
    for i, row in enumerate(frame):
        for j, cell in enumerate(row):
            if frame [i][j][0] > frame[i][j][1] and frame[i][j][0] > frame[i][j][2]:
                frame[i][j][:] = [255, 0 , 0]
            else:
                frame[i][j][0] = 0
    '''
    #frame= cv2.Canny(frame, 40, 200)
    frame[:][:][1:3] = cv2.GaussianBlur(frame[:][:][1:3], (13, 13), 0)
    #frame = cv2.bilateralFilter(frame,bilateral_size, bilateral_sigma_color, bilateral_sigma_space)
    if display_help:
        frame = cv2.putText(frame, 'This is help message', (50,50), cv2.FONT_HERSHEY_SIMPLEX,  1, (0,0,255), 2, cv2.LINE_AA)
    if pipe:
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        if sys.version_info.major == 3:
            sys.stdout.buffer.write(frame.tostring())
        else:
            sys.stdout.write( str(frame.tostring()) )
    else:
        cv2.imshow('output', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    
    if key & 0xFF == ord('i'):
        display_help = ~display_help
    if key & 0xFF == ord('w'):
        mode = 'width'      
    if key & 0xFF == ord('h'):
        mode = 'height'
        
    if mode == 'width':
        if key & 0xFF == ord('+'):
            w_scale += 1
        elif  key & 0xFF == ord('-'):
            w_scale -= 1
            
    if mode == 'height':
        if key & 0xFF == ord('+'):
            h_scale += 1
        elif  key & 0xFF == ord('-'):
            h_scale -= 1
        
stream.stop()



