import cv2
import numpy as np 
import os
import recognition

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
os.system("sync_time")

while True:

	cap = cv2.VideoCapture(0)

	var = 0

	while cap.read()[0]:
		ret, img = cap.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 3)

		if len(faces) == 0:
			var = 0

		else:
			var += 1

		print(var)

		if var == 20:
			break

	cap.release()

	print("record face started")
	command  = "ffmpeg -y -video_size 640x480 -i /dev/video0 -c copy -t 5 ./incomingVid/verifyMe.avi"
	os.system(command)

	recognition.recognise()
