import sys
from queue import Queue, Empty
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from threads.camera_thread import CameraThread
from pydispatch import dispatcher

from helpers import set_msg

class Camera(QWidget):
  def __init__(self, camera_handle):
    super().__init__()
    self.handle = camera_handle
    # ~ self.change_icon = change_icon
    self.initUI()
    self.init_thread()

  # display image emitted from camera thread
  @pyqtSlot(QImage)
  def set_img(self, image):
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
    
  def init_thread(self):
    self.thread = CameraThread(self.handle, self)      
    self.thread.changePixmap.connect(self.set_img)
    self.thread.send_msg.connect(set_msg)
    self.thread.start() 

  # explicit call vs called in the destructor
  def stop_thread(self):
    print("\nRequesting camera thread close...")
    self.thread.requestInterruption()
    self.thread.wait()
