import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QVBoxLayout
)

from widgets.camera_widget import Camera
from helpers import list_ports

class CameraTabs(QWidget):
  def __init__(self, cam_handles):
    super(CameraTabs, self).__init__()
    self.layout = QVBoxLayout()

    tabs = QTabWidget()
    tabs.setTabPosition(QTabWidget.North)
    tabs.setMovable(True)
    
    # auto detect cameras and add to list
    # ~ available_ports,working_ports,non_working_ports = list_ports()
    # ~ for n, cam in enumerate(working_ports):
      # ~ tabs.addTab(Camera(cam), "camera {}".format(n+1))
    
    for i in range(len(cam_handles)):
      print("cam",i,"available", cam_handles[i])
      tabs.addTab(Camera(cam_handles[i]), "Camera {}".format(i+1))
      
    self.layout.addWidget(tabs)
    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(10)
    self.setLayout(self.layout)
