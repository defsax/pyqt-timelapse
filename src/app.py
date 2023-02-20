import os 
import sys
import time
import cv2 as cv
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
  QApplication, 
  QMainWindow, 
  QWidget, 
  QVBoxLayout,
  QHBoxLayout, 
  QLabel,
  QPushButton,
  QComboBox
)
from PyQt5.QtCore import Qt

from widgets.camera_tabs import CameraTabs
from widgets.interval_widget import IntervalOptions
from widgets.duration_widget import DurationOptions
from widgets.filename_widget import FileNameBox
from widgets.location_widget import LocationOptions
from widgets.start_quit_widget import StartQuit
from widgets.status_widget import StatusBox

from threads.timelapse_thread import TimelapseThread
from threads.camera_thread_manager import CameraThreadManager

from helpers import list_ports


class MainWindow(QMainWindow):

  def __init__(self):
    super(MainWindow, self).__init__()
    self.cam_handles = []
    self.get_camera_handles()
    self.init_threads()
    self.init_options()
    self.init_ui()
      
  def __del__(self):
    print("\nApp unwind.")
    
  def get_camera_handles(self):
    # get available cameras
    available_ports,working_ports,non_working_ports = list_ports()
    
    # get cv handles
    for cam_id in working_ports:
      cap = cv.VideoCapture(cam_id, cv.CAP_V4L)
      self.cam_handles.append(cap)
  
  def init_threads(self):
    # pass cv handles to cam tabs and down to camera class / thread
    self.camera_manager = CameraThreadManager(self.cam_handles)
    
    # pass cv handles to timelapse thread
    self.timelapse_thread = TimelapseThread(self.cam_handles)
  
  def init_options(self):
    # set up cam_tabs by passing camera list
    self.cam_tabs = CameraTabs(self.camera_manager.cams)
    
    # set up which intervals are wanted (minutes)
    self.intervals = IntervalOptions(["1", "5", "30", "60", "180"])
    
    # set up which durations are wanted (minutes)
    self.durations = DurationOptions(["5", "25", "180", "360", "540", "960", "1020", "3840"])
    
    # initialize here so that StartQuit class can be passed to timelapse thread
    # in order to change button
    self.start_quit = StartQuit(self)
    
    # set up here to pass to timelapse thread
    self.file_name = FileNameBox(self)
    self.pics_location = LocationOptions(self)
    
    # set up status box
    self.status_box = StatusBox("Please enter file name and location.")
  
    
  def init_ui(self):
    # set up window settings
    self.setWindowTitle("pi timelapse app")
    self.setGeometry(2200, 300, 990, 535)
    
    # create layout containers
    container = QHBoxLayout()
    options = QVBoxLayout()
    
    # add all widgets
    options.addWidget(self.intervals, stretch=2)    
    options.addWidget(self.durations, stretch=2)
    options.addWidget(self.file_name, stretch=2)
    options.addWidget(self.pics_location, stretch=2)
    options.addWidget(self.status_box, stretch=1)
    options.addWidget(self.start_quit, stretch=1)
    
    # periodically check for cameras being hooked up
    # pass camera id to camera tabs widget (or have camera tabs do this)
    # dynamically add or remove camera view
    container.addWidget(self.cam_tabs, stretch=2)
    
    # set options style and add to container
    options.setContentsMargins(20, 10, 20, 10)
    container.addLayout(options, stretch=1)
    
    # dummy widget to hold layout, layout holds actual widgets
    widget = QWidget()
    widget.setLayout(container)
    
    # dummy widget used as central widget
    self.setCentralWidget(widget)
  
  def start_timelapse(self):
    # set widgets to disabled
    self.status_box.set_status("Started", "Green")
    print("Start", self.intervals.choice, "m intervals", self.durations.choice, "m duration")
      
    print(self.file_name.text_box.text())
      
    # check if location array has a filepath or name
    # ~ if getattr(self.pics_location.filepaths, 'size', len(self.pics_location.filepaths)) and self.file_name.text_box.text():
    
    self.timelapse_thread.setup(
      self.intervals.choice, 
      self.durations.choice, 
      self.start_quit.start_btn,
      self.file_name.text_box.text(),
      self.pics_location.filepath
    )
    self.timelapse_thread.start()
  
  def stop_timelapse(self):
    print("Stop")
    self.status_box.set_status("Ready", "Blue")
    self.timelapse_thread.stop()
    
  def check_start_enable(self):
    if not self.pics_location.filepath == "" and self.file_name.text_box.text():
      self.start_quit.start_btn.setEnabled(True)
      self.status_box.set_status("Ready", "Blue")
    else:
      self.start_quit.start_btn.setEnabled(False)
      self.status_box.set_status("Please enter file name and location.", "Black")
    
  def handle_close(self):
    self.stop_timelapse()
    # important!
    self.camera_manager.stop()
    self.close()
    
# ~ if __name__ == "__main__":
app = QApplication(sys.argv)
window = MainWindow()
window.show()
# ~ os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

sys.exit(app.exec())

