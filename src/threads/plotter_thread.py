import random
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtTest


class PlotterThread(QThread):
  # set up pyqtsignals
  changePixmap = pyqtSignal()
  send_msg = pyqtSignal(str, str)
  
  def __init__(self, parent):
    super(PlotterThread, self).__init__()
    self.parent = parent
    print(self.parent)
    
    self.times = []
    self.temps = []
    self.rand_nums = []

    self.limit = 40

  def run(self): 
    print("hello")
    while not self.isInterruptionRequested():
      self.update_plot()
    
  def update_plot(self):
      print(self.parent.sensors)
      for sensor in self.parent.sensors:
        port, rh, temp = sensor.get_data()
        print(port)
        
        self.temps.append(temp)
        
      
        # Drop off the first y element, append a new one.
        self.parent.ydata = self.parent.ydata[1:] + [random.randint(0, 10)]

        # Note: we no longer need to clear the axis.
        if self.parent.plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.parent.canvas.axes.plot(self.parent.xdata, self.parent.ydata, 'r')
            self.parent.plot_ref = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self.parent.plot_ref.set_ydata(self.parent.ydata)

        # Trigger the canvas to update and redraw.
        self.parent.canvas.draw()
        QtTest.QTest.qWait(1000)

  
