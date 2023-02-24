import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QComboBox
from PyQt5.QtGui import QPalette, QColor

from pydispatch import dispatcher

class StatusBox(QWidget):

  def __init__(self, default_msg):
    super(StatusBox, self).__init__()
    
    layout = QVBoxLayout()
    
    self.status = QLabel("hi")
    font = self.status.font()
    font.setPointSize(10)
    self.status.setFont(font)
    
    self.message = QLabel(default_msg)
    font = self.message.font()
    font.setPointSize(16)
    self.message.setFont(font)
    
    # ~ self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    self.message.setScaledContents(True)
    
    # ~ self.setAutoFillBackground(True)
    # ~ pal = self.palette()
    # ~ pal.setColor(QPalette.Window, QColor("red"))
    # ~ self.setPalette(pal)
    
    layout.addWidget(self.status)
    layout.addWidget(self.message)
    layout.setAlignment(Qt.AlignBottom)
    
    self.setLayout(layout)
    
    dispatcher.connect(self.set_status1, signal = "status_update", sender = dispatcher.Any)

  def set_status(self, msg, color="Black"):
    format_string = '<font color="{0}">{1}</font>'
    self.message.setText(format_string.format(color, msg))

  def set_status1(self, sender):
    text_color = sender["col"]
    message = sender["msg"]
    format_string = '<font color="{0}">{1}</font>'
    # ~ print("event status update", sender["msg"], sender["col"])
    self.message.setText(format_string.format(text_color, message))
