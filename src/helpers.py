from PyQt5.QtCore import pyqtSlot
from pydispatch import dispatcher
import cv2
import serial
import glob
# ~ import warnings
    
def list_cameras():
  """
  Test the ports and returns a tuple with the available ports and the ones that are working.
  """
  non_working_ports = []
  dev_port = 0
  working_ports = []
  available_ports = []
  
  while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
    # ~ with warnings.catch_warnings():
      # ~ warnings.simplefilter("ignore")
    try:
      camera = cv2.VideoCapture(dev_port, cv2.CAP_V4L)
    except:
      print("error")
    if not camera.isOpened():
      non_working_ports.append(dev_port)
      print("Port %s is not working." %dev_port)
    else:
      is_reading, img = camera.read()
      w = camera.get(3)
      h = camera.get(4)
      if is_reading:
        print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
        working_ports.append(dev_port)
      else:
        print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
        available_ports.append(dev_port)
    dev_port +=1
  return available_ports,working_ports,non_working_ports

def list_serial_devices():
    ports = glob.glob('/dev/ttyACM[0-9]*')
    res = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            res.append(port)
        except:
            pass
    return res

# dispatch message emitted from thread
@pyqtSlot(str, str)
def set_msg(msg, col):
  dispatcher.send(signal = "status_update", sender = {"msg":msg, "col": col} )



