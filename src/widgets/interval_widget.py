import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QComboBox


class IntervalOptions(QWidget):

  def __init__(self, interval_list):
    super(IntervalOptions, self).__init__()
    
    layout = QVBoxLayout()
    
    label = QLabel("Interval (Minutes)")
    font = label.font()
    font.setPointSize(12)
    
    label.setFont(font)
    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    label.setScaledContents(True)
    
    self.intervals = QComboBox()
    self.intervals.addItems(interval_list)
    self.intervals.activated.connect(self.handle_change)
    
    self.choice = str(self.intervals.currentText())
    
    layout.addWidget(label)
    layout.addWidget(self.intervals)
    layout.setAlignment(Qt.AlignTop)
    
    self.setLayout(layout)
  
  def handle_change(self, index):
    self.choice = str(self.intervals.currentText())
    print(self.choice)
    
