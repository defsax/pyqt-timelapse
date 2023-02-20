from PyQt5.QtWidgets import QWidget
  
from widgets.camera_widget import Camera

class CameraThreadManager(QWidget):
  def __init__(self, cam_handles):
    super(CameraThreadManager, self).__init__()
    self.cams = []
    self.create_cams(cam_handles)
    
  def create_cams(self, handles):
    for i in range(len(handles)):
      self.cams.append(Camera(handles[i]))
      
    print(self.cams)
    
  def stop(self):
    print("\nCamera threads stopping...")
    # check for if cams exist first...
    if not getattr(self.cams, 'size', len(self.cams)):
      print("No cameras to stop!")
      return
      
    for i, cam in enumerate(self.cams):
      cam.stop_thread()
      
