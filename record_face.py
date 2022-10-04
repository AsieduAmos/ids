import cv2
import numpy as np 
import sqlite3
import os
import pyrebase
import random
import string
import trainer

conn = sqlite3.connect('database.db',check_same_thread=False)
if not os.path.exists('./dataset'):
    os.makedirs('./dataset')

c = conn.cursor()

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')

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

startExtracting = False

def stream_handler(message):
	global startExtracting
	
	if startExtracting and message["data"]: 
		newPerson = message["data"]
		
		name = newPerson["name"]
		index = ''.join(random.choice(string.digits) for _ in range(5))
		relationship = newPerson["relationship"]
		video = newPerson["file_path"]
		
		print(index,name,relationship,video)
		train(index,name,relationship,video)
		
	startExtracting = True


my_stream = db.child("approved_access").stream(stream_handler)



def train(index,name,relationship,video):

	cap = cv2.VideoCapture(video)


	Fullname = name
	Id_number = index
	Relatioship = relationship
	c.execute('INSERT INTO Details(id_no,name,relationship) VALUES (?,?,?)', (Id_number,Fullname,Relatioship))


	uid = c.lastrowid
	print(uid)
	
	counter = 0
	
	try:

		while cap.read()[0]:
			ret, img = cap.read()
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			faces = face_cascade.detectMultiScale(gray, 1.2, 5)

			for (x,y,w,h) in faces:
				counter += 1
				cv2.imwrite(f"dataset/{Fullname}."+str(Id_number)+"."+str(counter)+".jpg",gray[y:y+h,x:x+w])
				cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 3)
				cv2.waitKey(100)
			cv2.imshow('img',img)
			if cv2.waitKey(10)== ord('q'):
				break
			
			if counter == 20:
				break

		cap.release()

		conn.commit()

		cv2.destroyAllWindows()

		trainer.startTrainer()
	
	except:
		print("an error occured")
