import pyttsx3
import pyrebase
import time

running = True
prev=""
delay=1


config = {
    "apiKey": "AIzaSyCmOMT9-Im4hxMHwgSRANC3ptbOLv4u5VM",
    "authDomain": "smartglasses-254516.firebaseapp.com",
    "databaseURL": "https://smartglasses-254516.firebaseio.com",
    "projectId": "smartglasses-254516",
    "storageBucket": "smartglasses-254516.appspot.com",
    "messagingSenderId": "582265500473",
    "appId": "1:582265500473:web:9ab01298f934eda073aee8",
    "measurementId": "G-DLFLL43SDP"
  }

firebase = pyrebase.initialize_app(config)

db = firebase.database()
#engine = pyttsx3.init()
#engine.setProperty('volume', 1)
#engine.setProperty('voice',"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

def stream_handler(message):
  print(message["event"]) # put
  print(message["path"]) # /-K7yGTTEp7O549EzTYtI
  print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
  data = message["data"]
  engine = pyttsx3.init()
  engine.setProperty('rate', 250)
  engine.say(str(data))
  engine.runAndWait()

while(running):
    obj = db.child("Objects").get()
    curr=obj.val()['text']
    print(curr)
    if curr != prev and curr != "":
        prev=curr
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(str(f"{curr} meters away"))
        engine.runAndWait()
    time.sleep(delay)
    #running = False

#my_stream = db.child("Objects").stream(stream_handler)

text = ''' Person at 2 meters
Truck at 3 meters  
Car at 6 meters  
Person at 12 meters  
Car at 15 meters  
Person at 20 meters  '''



# for i in range(10):
#     engine.say("1")
# #engine.runAndWait()

