from datetime import datetime
import numpy as np
import cv2
import os
import sched, time
from PyQt5.QtCore import QThread, pyqtSignal

try:
  import RPi.GPIO as GPIO
except ImportError:
  print("Not running on raspberry pi.")

class TimelapseThread(QThread):
  set_msg = pyqtSignal(str, str)
  set_status = pyqtSignal(str, str)
  
  def __init__(self, cam_handles, sensors):
    super(TimelapseThread, self).__init__()
    
    self.is_rpi = os.uname()[1] == "raspberrypi"
    
    if self.is_rpi:
      print('raspberry pi:',self.is_rpi)
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
    self.sensors = sensors
    self.scheduler = sched.scheduler(time.time, time.sleep)
    
  def setup(self, interval, duration, button, file_name, location):
    self.button = button
    self.interval = int(interval) * 60
    self.duration = int(duration) * 60
    
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
    
    # set up data file
    try:
      with open(self.path + "/data.txt", "a") as f:
        f.write("time,humidity,temperature,image_id\n")
        f.close()
    except:
      print("write setup error")
    
    # register events from start to end at designated intervals and duration
    while iterator_time < end_time:
      self.count += 1
      self.scheduler.enterabs(iterator_time, 1, self.take_pictures, argument=(self.count,))
      self.scheduler.enterabs(iterator_time, 2, self.log_data, argument=(self.count,))
      iterator_time += self.interval
  
  def take_pictures(self, count):
    if self.is_rpi:
      # turn on rpi gpio pin 14
      GPIO.output(14,GPIO.HIGH)
    
    print("\nTime: ", time.ctime())
    
    # loop cameras and take pictures
    for i, cap in enumerate(self.cam_folders):
      start = datetime.now()
      date_time = start.strftime("%m-%d-%Y_%H-%M-%S")
      try:
        # Capture a frame ret, img = cap.read()
        ret, frame = cap.read()
        
        # save file
        cv2.imwrite(self.cam_folders[cap]+'/'+date_time+'_img'+str(count).zfill(4)+'.png', frame)
        
        # print out, send to status box
        print("cam", i+1, "picture", count, "taken")
        format_string = "Camera {0} picture {1} taken"
        self.set_msg.emit(format_string.format(i+1, count), "Black")
      
      except:
        print("error capturing cam", i+1, "picture", count)
        format_string = "Error: camera {0} picture {1} not captured!"
        self.set_msg.emit(format_string.format(i+1, count), "Red")
      
    if self.is_rpi:
      # turn off rpi gpio pin 14
      GPIO.output(14,GPIO.LOW)
      
  def log_data(self, count):
      # log temp and rh for each sensor          
      for i, sensor in enumerate(self.sensors):
          rh, temp = sensor.get_data()
          print("logging:", temp, rh)
          try:
              start = datetime.now()
              date_time = start.strftime("%m-%d-%Y_%H-%M-%S")
              print(self.path)
              with open(self.path + "/data.txt", "a") as f:
                  f.write(date_time + ",")
                  f.write(rh + ",")
                  f.write(temp + ",")
                  f.write("img" + str(count).zfill(4)+".png\n")
                  f.close()
          except:
            print("error")
  def run(self):
    self.scheduler.run(blocking = True)
    self.button.setText("Start")
    print("Time lapse done!")
    
    # emit finished signal to status box
    self.set_msg.emit("Time lapse done!", "Green")
    self.set_status.emit("Ready...", "Blue")
    
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
