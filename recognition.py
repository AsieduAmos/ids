import cv2
import numpy as np
import sqlite3
import os
import pyrebase
from time import ctime
import uuid

firebaseConfig = {
  'apiKey': "AIzaSyDnlI2tmTITBlhhQmgYlAETtT5-JHV6kJg",
  'authDomain': "ilarm-c4a28.firebaseapp.com",
  'databaseURL': "https://ilarm-c4a28-default-rtdb.firebaseio.com",
  'projectId': "ilarm-c4a28",
  'storageBucket': "ilarm-c4a28.appspot.com",
  'messagingSenderId': "938220116599",
  'appId': "1:938220116599:web:d2158ac593b7862c640472",
  'measurementId': "G-32SJE4HR19"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

conn = sqlite3.connect('database.db')
c = conn.cursor()

def recognise():

	c.execute("SELECT * FROM Details")
	print(c.fetchall())

	fname = "./recognizer/trainingData.yml"

	if not os.path.isfile(fname):
    		print("Please train the data first")
	    	exit(0)

	face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')

	cap = cv2.VideoCapture('./incomingVid/verifyMe.avi')
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read(fname)

	person_is_known = False
	name = ""
	relationship = ""
	
	try:

		while cap.read()[0]:
			ret, img = cap.read()
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray, 1.3, 3)
			for (x,y,w,h) in faces:
				cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
				ids,conf = recognizer.predict(gray[y:y+h,x:x+w])

				c.execute("SELECT name FROM Details WHERE  id_no = (?)", (ids,))
				result1 = c.fetchone()
				result1 = "+".join(result1)

				c.execute("SELECT relationship FROM Details WHERE  id_no = (?)", (ids,))
				result2 = c.fetchone()
				result2 = "+".join(result2)


				if conf < 40:
					cv2.putText(img, f"Name: {result1}", (x,y-90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,255,0),2)
					cv2.putText(img, f"relationship: {result2}", (x,y-55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,255,0),2)
					cv2.putText(img, f"Distance: {conf}", (x,y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,255,0),2)

					person_is_known = True
					name = result1
					relationship = result2
				else:
					cv2.putText(img, 'UNKWON PERSON DETECTED', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255),2)

	except:
		print("error occured...ignoring")

	cap.release()

	if person_is_known : #upload details of person to server
		print("\n\n\nperson identified as " + name + " with relationship as " + relationship + "\n\n\n")
		data = {"name": name,"relationship":relationship,"time":ctime()}
		try:
			db.child("entry_logs").push(data)
		except:
			print("network error...could not update login info to server")
	else: #sound alarm, upload intruder details to server
		print("\n\n\nperson unknown\n\n")
		os.system("ffmpeg -y -f v4l2 -video_size 1280x720 -i /dev/video0 -frames 1 ./incomingVid/intruder.jpg")
		try:
			storage_prefix = "https://firebasestorage.googleapis.com/v0/b/ilarm-c4a28.appspot.com/o/intruders%2F"
			storage_postfix = "?alt=media"
			return_value = storage.child("intruders/" + uuid.uuid4().hex + ".jpg").put("./incomingVid/intruder.jpg")
			original_filename = return_value["name"].replace("intruders/","")
			
			storage_filename = storage_prefix + original_filename + storage_postfix
			print(storage_filename)
			db.child("intruder").update({"url":storage_filename})

		except:
			print("network error...could not update intruder info to server")
		os.system("python3 buzzer.py")
