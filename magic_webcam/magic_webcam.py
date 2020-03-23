import cv2
import sys
import numpy as np
import argparse
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
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # floa
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
stream.start(queue_length)

while True:

    #ok, frame = cap.read()
    frame = stream.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    if not ok:
        break
    frame = cv2.warpAffine(frame,warp_mat, ( int(width) , int(height)))
    
    if pipe:
        if sys.version_info.major == 3:
            sys.stdout.buffer.write(frame.tostring())
        else:
            sys.stdout.write( str(frame.tostring()) )
    else:
        cv2.imshow('output', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

stream.stop()


"""
python2 pipetest.py | ffmpeg -f rawvideo -pixel_format bgr24 -video_size 1280x720erate 30 -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 -vf 'scale=1280:720' -pixel_format rgb24 /dev/video1


"""
