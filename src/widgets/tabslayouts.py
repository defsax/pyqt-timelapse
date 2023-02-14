
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QHBoxLayout,
    QPushButton,
    QTabWidget,
    QWidget,
)

from color_widget import Color

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("My App")
    self.setGeometry(2900, 700, 500, 400)

    h_layout = QHBoxLayout()

    label = QLabel("stuff")
    h_layout.addWidget(label)

    tabs = QTabWidget()
    tabs.setTabPosition(QTabWidget.North)
    tabs.setMovable(True)

    for n, color in enumerate(["red", "green", "blue", "yellow"]):
      tabs.addTab(Color(color), color)

    h_layout.addWidget(tabs)
    
    
    #dummy widget to hold layout, layout holds actual widgets
    widget = QWidget()
    widget.setLayout(h_layout)
    
    #dummy widget used as central widget
    self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
