# Image Sender
import pyrebase
import io
import time
import requests
import sys
import numpy as np
import cv2

count = 0
running = True
delay = 0.2
resolution = None #(1000,1000)
scaling_factor=1
buffer_size = 2


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
storage=firebase.storage()

snapObj = cv2.VideoCapture(0)

while (running):
  res,snapshot=snapObj.read()
  #snapshot = cv2.imread("/content/image.png")
  snapshot = cv2.resize(snapshot, resolution, fx=scaling_factor, fy=scaling_factor)
  res = cv2.imwrite(fr"a{count}.jpg",snapshot)
  a=storage.child(f"image/a{count}.jpg").put(f"a{count}.jpg")
  print("Image sent : ",a["name"]," ",int(a["size"])/1000," KB")
  time.sleep(delay)
  count = (count + 1) % buffer_size
snapObj.release()
