from PyQt5.QtCore import QThread, pyqtSignal
from pyfirmata import Arduino, util

# https://pypi.org/project/pyFirmata/

class ArduinoThread(QThread):
  def __init__(self, board):
    super(ArduinoThread, self).__init__()
    # ~ self.board = board      
    
  def run(self): 
    print("arduino thread started")
    # ~ it = util.Iterator(self.board)
    # ~ it.start()
    # ~ print("iterator started")
    # ~ self.board.analog[0].enable_reporting()
    # ~ self.board.analog[0].read()
