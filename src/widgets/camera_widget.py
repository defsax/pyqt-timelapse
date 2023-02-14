import cv2 as cv
import sys
from queue import Queue, Empty
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

class Thread(QThread):
  changePixmap = pyqtSignal(QImage)
  def __init__(self, handle):
    super(Thread, self).__init__()
    self.handle = handle
    # ~ self.cap = cv.VideoCapture(self.id, cv.CAP_V4L)

  def run(self):     
    while not self.isInterruptionRequested():
      ret, frame = self.handle.read() 
      if self.isInterruptionRequested():
        print("cam thread interruption requested")
        break
        
      if ret:        
        # https://stackoverflow.com/a/55468544/6622587
        rgbImage = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # ~ rgbImage = cv.cvtColor(frame, cv.COLOR_RGBA2GRAY)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.changePixmap.emit(p)
      else:
        print("Can't receive frame (stream end?). Exiting ...")
        break
        
    self.handle.release()
    cv.destroyAllWindows()
    print("camera thread closed. all done.")

class Camera(QWidget):
  def __init__(self, camera_handle):
    super().__init__()
    self.handle = camera_handle
    self.initUI()
    self.initThread()
  
  def __del__(self):
    print("\nrequesting camera thread close...")
    self.th.requestInterruption()
    self.th.wait()


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
    self.th = Thread(self.handle)
    
    # ~ if self.th.cap is None or not self.th.cap.isOpened():
      # ~ print('Warning: unable to open video source: ', self.th.cap)
      # ~ self.deleteLater()
      
    self.th.changePixmap.connect(self.setImage)
    self.th.start() 
