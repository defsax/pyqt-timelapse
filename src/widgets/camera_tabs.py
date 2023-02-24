import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QStyle
)

from widgets.camera_widget import Camera
from pydispatch import dispatcher

class CameraTabs(QWidget):
  def __init__(self, cameras):
    super(CameraTabs, self).__init__()
    
    self.layout = QVBoxLayout()

    self.tabs = QTabWidget()
    self.tabs.setTabPosition(QTabWidget.North)
    # ~ tabs.setIconSize(QSize(20,20))
    self.tabs.setMovable(True)
    
    # create icons
    check_pixmap = QStyle.SP_DialogApplyButton
    x_pixmap = QStyle.SP_MessageBoxCritical
    
    self.check_icon = self.style().standardIcon(check_pixmap)
    self.x_icon = self.style().standardIcon(x_pixmap)
    
    # add camera widget array to tab list
    self.add_cams_to_tabs(cameras)
    
    # set layout and style
    self.layout.addWidget(self.tabs)
    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(10)
    self.setLayout(self.layout)
    
    # function to run when signal is received from cam disconnect
    dispatcher.connect(self.change_icon, signal = "cam_disconnect", sender = dispatcher.Any)
    
  # ~ def create_cams(self, cam_handles):
    # ~ for i in range(len(cam_handles)):
      # ~ self.cams.append(Camera(cam_handles[i], self.change_icon))
  
  def add_cams_to_tabs(self, cameras):
    for i, cam in enumerate(cameras):
      self.tabs.addTab(cam, self.check_icon, "Camera {}".format(i+1))
  
  def change_icon(self, sender):
    index = self.tabs.indexOf(sender)
    self.tabs.setTabIcon(index, self.x_icon)
    print("Camera disconnected", sender, index)
    
