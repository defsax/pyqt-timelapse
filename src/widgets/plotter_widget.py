import sys
import matplotlib
import random
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from threads.plotter_thread import PlotterThread


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Plotter(QtWidgets.QMainWindow):

    def __init__(self, sensors):
        super(Plotter, self).__init__()
  
        self.sensors = sensors
        
        
        
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        # ~ sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.setCentralWidget(self.canvas)
        
        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]
        
        self.plot_ref = None
        # ~ self.update_plot()

        self.show()
        self.p_thread = PlotterThread(self)
        self.p_thread.start()
        
        # ~ self.timer = QtCore.QTimer()
        # ~ self.timer.setInterval(100)
        # ~ self.timer.timeout.connect(self.update_plot)
        # ~ self.timer.start()
        
    # ~ def update_plot(self):
        # ~ for sensor in self.sensors:
          # ~ print(sensor.get_data())
          
        
        # ~ # Drop off the first y element, append a new one.
        # ~ self.ydata = self.ydata[1:] + [random.randint(0, 10)]

        # ~ # Note: we no longer need to clear the axis.
        # ~ if self.plot_ref is None:
            # ~ # First time we have no plot reference, so do a normal plot.
            # ~ # .plot returns a list of line <reference>s, as we're
            # ~ # only getting one we can take the first element.
            # ~ plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
            # ~ self.plot_ref = plot_refs[0]
        # ~ else:
            # ~ # We have a reference, we can use it to update the data for that line.
            # ~ self.plot_ref.set_ydata(self.ydata)

        # ~ # Trigger the canvas to update and redraw.
        # ~ self.canvas.draw()
