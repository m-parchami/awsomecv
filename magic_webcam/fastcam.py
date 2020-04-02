import cv2
import sys
from threading import Thread
if sys.version_info.major == 3:
    import queue
else:
    import Queue as queue
    
class Stream:

    def __init__(self, source = 0):

        self.cap = cv2.VideoCapture(source)
        self.current_size = 0
        if not self.cap.isOpened():

            print('something went wrong while openning source')
            exit(0)

        self.release = False


    def start(self, queue_size = 5):

        self.frame_queue = queue.Queue(queue_size)
        Thread(target = self.flow).start()
            
    def flow(self):
        
        while True:
            
            if self.release:
                break
            
            if self.frame_queue.full():
                #print('missed a frame because queue is full!')
                continue
            
            ok, frame = self.cap.read()
        
            if not ok:
                print('no more frames from source!')
                self.stop()

            self.frame_queue.put(frame)
            self.current_size += 1

        self.cap.release()
        exit(0)
    def read(self):
        self.current_size -= 1
        return self.frame_queue.get()
    
    
    def stop(self):
        self.release = True
        

"""
stream = Stream(0)
stream.start(10)

while True:

    img = stream.read()
    
    img = cv2.putText(img, 'queue len: '+ str(stream.current_size), (50,50), cv2.FONT_HERSHEY_SIMPLEX,  1, (0,0,255), 2, cv2.LINE_AA)
    
    cv2.imshow('webcam',img)
    key = cv2.waitKey(1)

    if key & 0xFF == ord('q'):

        stream.stop()
        break

cv2.destroyAllWindows()
""" 
