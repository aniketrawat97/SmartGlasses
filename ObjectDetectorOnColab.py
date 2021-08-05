# Run this file on Google Colab 
# Firebase

import cv2
import PIL
import time
from os import path
import numpy as np
import os
from PIL import Image , ImageChops
from pydarknet import Detector, Image as darkImage
from IPython.display import Image as ColabImage

import pyrebase
import io
import requests


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
db = firebase.database()

def equal(im1, im2): #
    if type(im1) == "numpy.ndarray":
      im1= PIL.Image.fromarray(im1[:,:,::-1])
    if type(im2) == "numpy.ndarray":
      im2= PIL.Image.fromarray(im2[:,:,::-1])

    return ImageChops.difference(im1, im2).getbbox() is None

def detect_object(img): # cv2 image
  pil_image = PIL.Image.fromarray(img[:,:,::-1])
  img_darknet = darkImage(img)
  results = net.detect(img_darknet)
  return results # in format { category , score , bounds }

def initilizeDetector():
  return Detector( bytes("./cfg/yolov3.cfg", encoding="utf-8"),
                bytes("./weights/yolov3.weights", encoding="utf-8"),
                0,
                bytes("./cfg/coco.data",encoding="utf-8"))

def calculate_distance(width,focal,pix):
  return width * focal/pix

def calculate_focallength(width,dist,pix):
  return pix * dist / width

####  VARIABLES TO TUNE THE SYSTEM ####

#input_image_path = f"/content/drive/My Drive/Images/a0.jpg"
#output_textfile_path = f"/content/drive/My Drive/Images/outtext.txt"
running = True
use_buffer = True
buffer_size = 2
file_scan_delay = 0 # in sec
detection_delay = 0 # in sec
scaling_factor = 1
image_shrinkage_factor = 1
number_of_labels_to_send = 5 # items are sent in order closest to farthest
focal_length = 620 # in mm , calculate using the function calculate_focallength

label_list=['car','person','motorbike','bus','truck','bicycle','cat','dog','bottle']

width_dict={}
width_dict['car'] = 2
width_dict['person'] = 0.5
width_dict['cat'] = 0.5
width_dict['dog'] = 0.7
width_dict['bus'] = 5.5
width_dict['truck'] = 5.5
width_dict['motorbike'] = 1.8
width_dict['traffic light'] = 0.2
width_dict['bicycle'] = 1
width_dict['bottle'] = 0.05

####  DO NOT CHANGE BELOW THIS POINT UNLESS YOU REALLY KNOW WHAT YOU'RE DOING ####

prev_img=None

net = initilizeDetector()
#prev_img = cv2.imread("/content/drive/My Drive/Images/a3.jpg")
count=0

while running:
  #if use_buffer:
    #input_image_path = f"/content/drive/My Drive/Images/a{count}.jpg"
    #output_textfile_path = f"/content/drive/My Drive/Images/outtext{count}.txt"

  url = storage.child(f"image/a{count}.jpg").get_url(None)
  #print(url)

  r = requests.get( url, timeout = 2 )

  while r.status_code != requests.codes.ok:
    r = requests.get( url, timeout = 2 )
    print(f"Waiting for image from pi")
    time.sleep(file_scan_delay)

  imPIL = Image.open(io.BytesIO(r.content))

  # while not path.exists(input_image_path):
  #   print(f"Waiting for image to be written")
  #   time.sleep(file_scan_delay)
    
  # img = cv2.imread(input_image_path)

  img = cv2.cvtColor(np.array(imPIL), cv2.COLOR_RGB2BGR)

  img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor) # TO RESIZE IMAGE (INCREASES PROCESSING SPEED)
  count = ( count + 1 ) % buffer_size
  print(count)

  if prev_img is not None :

    if not np.array_equiv(img,prev_img):
      results = detect_object(img)
      img_output = img.copy()

      out=""
      sent_items=0
      item_list=[]
      for cat, score, bounds in results:
        x, y, w, h = bounds
        cv2.rectangle(img_output, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
        cv2.putText(img_output,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
        print(f"{cat},{score},{bounds}")
        if cat.decode("utf-8") in label_list:
          dist = calculate_distance(width_dict[cat.decode("utf-8")] * 1000 * image_shrinkage_factor,focal_length,w)/1000
          item_list.append([cat.decode("utf-8"),int(dist)])
          
      item_list.sort( key=lambda x:x[1] )
      print(item_list)
      for i in range( min(number_of_labels_to_send,len(item_list))):
        out = out + f" {item_list[i][0]} {item_list[i][1]}"

      data ={}
      data["text"] = out
      db.child("Objects").set(data)


      pil_image_output = PIL.Image.fromarray(img_output[:,:,::-1])
      display(pil_image_output)
    else:
      print("Repeated Image , Skipped")
      
  prev_img = img
  time.sleep(detection_delay)
  # if input() == 'q':
  #   running=False
  #   print("Quitting")