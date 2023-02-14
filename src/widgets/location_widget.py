import sys

from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import (
  QLabel, 
  QWidget, 
  QVBoxLayout, 
  QHBoxLayout, 
  QFileDialog, 
  QPushButton, 
  QLineEdit
)


class LocationOptions(QWidget):

  def __init__(self, parent):
    super(LocationOptions, self).__init__()
    self.dirpath = QDir.currentPath()
    self.filepath = ""
    self.parent = parent
    
    # layouts
    layout = QVBoxLayout()
    search = QHBoxLayout()
    
    # label and font settings
    label = QLabel("Location")
    font = label.font()
    font.setPointSize(12)
    
    label.setFont(font)
    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    label.setScaledContents(True)
    
    # text box to display chosen folder
    self.location = QLineEdit(self)
    self.location.setReadOnly(True)
    
    # button to open file browser dialog
    button = QPushButton('Select')
    button.clicked.connect(self.getFile)
    
    # add text box and button for folder choosing
    search.addWidget(self.location)
    search.addWidget(button)
    
    layout.addWidget(label)
    layout.addLayout(search)
    layout.setAlignment(Qt.AlignTop)
    
    self.setLayout(layout)
  
  def getFile(self):
    # ~ self.filepaths = []
    # ~ self.filepaths.append(QFileDialog.getExistingDirectory(self, caption='Choose Directory',
                                                # ~ directory=self.dirpath))
                                                
    self.filepath = QFileDialog.getExistingDirectory(self, caption='Choose Directory',
                                                directory=self.dirpath)
    
    if self.filepath == "":
      return
    else:
      print(self.filepath)
      self.location.setText(self.filepath)
    
    # error handling: checks whether start button should be enabled
    self.parent.check_start_enable()

