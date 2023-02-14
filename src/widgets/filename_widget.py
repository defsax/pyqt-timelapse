import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QLineEdit



class FileNameBox(QWidget):

  def __init__(self, parent):
    super(FileNameBox, self).__init__()
    
    layout = QVBoxLayout()
    
    label = QLabel("File Name")
    font = label.font()
    font.setPointSize(12)
    
    label.setFont(font)
    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    label.setScaledContents(True)
    
    self.text_box = QLineEdit()
    self.text_box.setMaxLength(100)
    self.text_box.setPlaceholderText("Enter file name")
    # error handling: checks whether start button should be enabled
    self.text_box.textChanged.connect(parent.check_start_enable)
    self.is_empty = True
    
    layout.addWidget(label)
    layout.addWidget(self.text_box)
    layout.setAlignment(Qt.AlignTop)
    
    self.setLayout(layout)
    

