import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QComboBox


class DurationOptions(QWidget):

  def __init__(self, duration_list):
    super(DurationOptions, self).__init__()
    
    layout = QVBoxLayout()
    
    label = QLabel("Total Duration (Minutes)")
    font = label.font()
    font.setPointSize(12)
    
    label.setFont(font)
    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    label.setScaledContents(True)
    
    self.durations = QComboBox()
    self.durations.addItems(duration_list)
    self.durations.activated.connect(self.handle_change)
    
    self.choice = str(self.durations.currentText())
    
    layout.addWidget(label)
    layout.addWidget(self.durations)
    layout.setAlignment(Qt.AlignTop)
    
    self.setLayout(layout)

  def handle_change(self, index):
    self.choice = str(self.durations.currentText())
    print(self.choice)
