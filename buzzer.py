import RPi.GPIO as GPIO
from time import sleep
from threading import Timer
import pyrebase
import os

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

def stream_handler(message):
	if message["data"]:
		data = message["data"]
		if data == 1 :
			db.child("stopAlarm").update({"value":0})
			print("alarm stopped")
			stopAlarm()

my_stream = db.child("stopAlarm").stream(stream_handler)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer=14
GPIO.setup(buzzer,GPIO.OUT)

activateBuzzer = True

def stopAlarm():
	global activateBuzzer
	activateBuzzer = False
	GPIO.output(buzzer,GPIO.LOW)
	os._exit(0)

def soundAlarm():
	a.start()
	while activateBuzzer:
		GPIO.output(buzzer,GPIO.HIGH)
		sleep(0.1)
		GPIO.output(buzzer,GPIO.LOW)
		sleep(0.1)

a = Timer(60,stopAlarm)
soundAlarm()
