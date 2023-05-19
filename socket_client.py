from time import sleep
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db
from socket import *
cred = credentials.Certificate('D:\json\graduation-bcd1c-firebase-adminsdk-26dai-e6dfa5b647.json')
firebase_admin.initialize_app(cred,
{
'databaseURL': 'https://graduation-bcd1c-default-rtdb.firebaseio.com/'
})
ref = db.reference('sensor/ECG')
ref2=db.reference('sensor/heartecg')
while True:
    sleep(10)
    sock = socket()
    sock.connect(("localhost", 9999))
    heart_rate = str(ref.get())
    ecg=str(ref2.get())
    sock.send(heart_rate.encode('utf8'))
    sock.send(ecg.encode('utf8'))
    sock.close()
