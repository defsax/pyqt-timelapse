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
    self.interval = int(interval) * 60
    self.duration = int(duration) * 60
    
    print(file_name, location)
    
    # get and format date
    start = datetime.now()
    self.date_time = start.strftime("%m-%d-%Y_%H-%M-%S")
    self.folder_name = file_name + "_" + self.date_time
    print("date and time:", self.date_time)

    # create and name folder for round of pictures after date
    # ~ photo_directory = "../pics/"
    photo_directory = location
    self.path = os.path.join(photo_directory, self.folder_name)
    os.makedirs(self.path)
    print(self.path)
    
    
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
    for i in range(len(self.cam_handles)):
      try:
        # Capture a frame ret, img = cap.read()
        ret, frame = self.cam_handles[i].read()
        # save file
        cv2.imwrite(self.path+'/img_'+str(count).zfill(4)+'cam_'+str(i+1).zfill(2)+'.png', frame)
        #print out
        print("cam", i+1, "picture", count, "taken")
      except:
        print("error capturing cam", i+1, "picture", count)
      
    GPIO.output(14,GPIO.LOW)

  def run(self):
    self.scheduler.run(blocking = True)
    self.button.setText("Start")
    print("time lapse done")
    
  def stop(self):
    print("timelapse thread stopping...")
    if self.scheduler.empty():
      print("no items to cancel!")
      return 
    else:
      for item in self.scheduler.queue:
        print("cancelling item...")
        self.scheduler.cancel(item)
      print("items cancelled.")
