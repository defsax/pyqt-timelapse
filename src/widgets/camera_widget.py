import sys
from queue import Queue, Empty
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from threads.camera_thread import CameraThread

class Camera(QWidget):
  def __init__(self, camera_handle):
    super().__init__()
    self.handle = camera_handle
    self.initUI()
    self.initThread()
  
  def __del__(self):
    print("\nrequesting camera thread close...")
    self.thread.requestInterruption()
    self.thread.wait()


  @pyqtSlot(QImage)
  def setImage(self, image):
    self.label.setPixmap(QPixmap.fromImage(image))

  def initUI(self):
    # self.setWindowTitle(self.title)
    # self.setGeometry(self.left, self.top, self.width, self.height)
    # self.resize(1800, 1200)
    # create a label
    self.label = QLabel(self)
    
    # self.label.move(280, 120)
    self.label.resize(640, 480)

    self.show()
    
  def initThread(self):
    self.thread = CameraThread(self.handle)      
    self.thread.changePixmap.connect(self.setImage)
    self.thread.start() 
