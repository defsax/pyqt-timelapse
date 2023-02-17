import cv2 as cv

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

class CameraThread(QThread):
  changePixmap = pyqtSignal(QImage)
  def __init__(self, handle):
    super(CameraThread, self).__init__()
    self.handle = handle

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
