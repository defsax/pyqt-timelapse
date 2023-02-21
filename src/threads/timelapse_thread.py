from datetime import datetime
import numpy as np
import cv2
import os
import sched, time
from PyQt5.QtCore import QThread

import RPi.GPIO as GPIO

class TimelapseThread(QThread):
  def __init__(self, cam_handles):
    super(TimelapseThread, self).__init__()
    
    # init gpio pins on the pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(14,GPIO.OUT)
    
    """
      VideoCapture object is created in app.py py and shared between 
      live camera and camera timelapse classes
      
      self.cap = cv2.VideoCapture(0)
    """
  
    self.cam_handles = cam_handles
    self.scheduler = sched.scheduler(time.time, time.sleep)
    
  def setup(self, interval, duration, button, file_name, location):
    self.button = button
    self.interval = int(interval) #* 60
    self.duration = int(duration) #* 60
    
    # ~ print(file_name, location)
    
    # get and format date
    start = datetime.now()
    self.folder_time = start.strftime("%m-%d-%Y_%H-%M-%S")
    self.folder_name = file_name + "_" + self.folder_time


    # create and name folder for round of pictures after date
    photo_directory = location
    self.path = os.path.join(photo_directory, self.folder_name)
    os.makedirs(self.path)
    
    # create dictionary to hold cam_handle and file location
    self.cam_folders = {}
    
    # create a folder for each camera
    for i in range(len(self.cam_handles)):
      camera_directory = "cam_" + str(i+1).zfill(2)
      cam_path = os.path.join(self.path, camera_directory)
      os.makedirs(cam_path)
      self.cam_folders.update({self.cam_handles[i]: cam_path})
    
    # set up interval and duration to figure out when to schedule photos
    iterator_time = time.time()
    end_time = time.time() + self.duration
    self.count = 0
    
    # register events from start to end at designated intervals and duration
    while iterator_time < end_time:
      self.count += 1
      self.scheduler.enterabs(iterator_time, 1, self.take_pictures, argument=(self.count,))
      iterator_time += self.interval
  
  def take_pictures(self, count):
    GPIO.output(14,GPIO.HIGH)
    print("\nTime: ", time.ctime())
    # loop cameras and take pictures
    # ~ for i in range(len(self.cam_handles)):
    for i, cap in enumerate(self.cam_folders):
      start = datetime.now()
      date_time = start.strftime("%m-%d-%Y_%H-%M-%S")
      try:
        # Capture a frame ret, img = cap.read()
        ret, frame = cap.read()
        # save file
        # ~ cv2.imwrite(self.path+'/cam_'+str(i+1).zfill(2)+'_img_'+str(count).zfill(4)+'.png', frame)
        cv2.imwrite(self.cam_folders[cap]+'/'+date_time+'_img'+str(count).zfill(4)+'.png', frame)
        #print out
        print("cam", i+1, "picture", count, "taken")
      except:
        print("error capturing cam", i+1, "picture", count)
      
    GPIO.output(14,GPIO.LOW)

  def run(self):
    self.scheduler.run(blocking = True)
    self.button.setText("Start")
    print("Time lapse done!")
    
    # emit finished signal to status box
    
    # run create video function and pass file path(s)
    
  def stop(self):
    print("\nTimelapse thread stopping...")
    if self.scheduler.empty():
      print("No items to cancel!")
      return 
    else:
      for item in self.scheduler.queue:
        print("Cancelling item...")
        self.scheduler.cancel(item)
      print("Items cancelled.")
