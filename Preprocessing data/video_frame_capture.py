#! python3
# video_frame_capture.py - capture frame from video for data collection

import cv2, time
import os.path

# search for path for video
path = os.getcwd() + '\\video\\'

if not os.path.exists(path):
    os.makedirs('video')

# create output folder for video frame capture to be saved
frame_path = os.getcwd() + '\\frame\\'

if not os.path.exists(frame_path):
    os.makedirs('frame')


# use cv2 to capture frame from video
fps = 5
count = 1

cap = cv2.VideoCapture(path)

if cap.isOpened() == False:
    print('Error! Cannot opened the video file.')

while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        time.sleep(1/fps)
        filename = count + '.jpg'
        cv2.imwrite(frame_path + filename, frame)
        count += 1
        
cap.release()
