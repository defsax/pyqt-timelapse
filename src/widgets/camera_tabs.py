import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QStyle
)
# ~ from PyQt5.QtGui import (
  # ~ QPixmap, 
  # ~ QIcon, 
  # ~ QColor, 
  # ~ QPainterPath, 
  # ~ QPainter,
  # ~ QBrush,
  # ~ QPen
# ~ )

from widgets.camera_widget import Camera
from helpers import list_ports

class CameraTabs(QWidget):
  def __init__(self, cam_handles):
    super(CameraTabs, self).__init__()
    
    self.layout = QVBoxLayout()

    tabs = QTabWidget()
    tabs.setTabPosition(QTabWidget.North)
    # ~ tabs.setIconSize(QSize(20,20))
    tabs.setMovable(True)
    
    check_pixmap = QStyle.SP_DialogApplyButton
    x_pixmap = QStyle.SP_MessageBoxCritical
    
    check_icon = self.style().standardIcon(check_pixmap)
    x_icon = self.style().standardIcon(x_pixmap)
    
    ##
    cam1 = Camera(cam_handles[0])
    tabs.addTab(cam1, check_icon, "Camera {}".format(0))
    cam2 = Camera(cam_handles[1])
    tabs.addTab(cam2, check_icon, "Camera {}".format(1))
    
    
    ##
    
    # ~ for i in range(len(cam_handles)):
      # ~ print("cam",i,"available", cam_handles[i])
      # ~ tabs.addTab(Camera(cam_handles[i]), x_icon, "Camera {}".format(i+1))
    
    self.layout.addWidget(tabs)
    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(10)
    self.setLayout(self.layout)
    
    # ~ page1 = tabs.indexOf(Camera)
    index1 = tabs.indexOf(cam1)
    index2 = tabs.indexOf(cam2)
    tabs.setTabIcon(index1, x_icon)
    # ~ page3 = tabs.findChild(QWidget, "Camera 3")
    print(index1, index2)
