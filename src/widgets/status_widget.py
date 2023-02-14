import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtGui import QPalette, QColor


class StatusBox(QWidget):

  def __init__(self, default_msg):
    super(StatusBox, self).__init__()
    
    layout = QVBoxLayout()
    
    self.label = QLabel(default_msg)
    font = self.label.font()
    font.setPointSize(16)
    
    self.label.setFont(font)
    # ~ self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    self.label.setScaledContents(True)
    
    # ~ self.setAutoFillBackground(True)
    # ~ pal = self.palette()
    # ~ pal.setColor(QPalette.Window, QColor("red"))
    # ~ self.setPalette(pal)
    
    layout.addWidget(self.label)
    layout.setAlignment(Qt.AlignBottom)
    
    self.setLayout(layout)

  def set_status(self, msg, color="Black"):
    format_string = '<font color="{0}">{1}</font>'
    self.label.setText(format_string.format(color, msg))
