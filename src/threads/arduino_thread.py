from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, QIODevice
from PyQt5.QtSerialPort import QSerialPort



class ArduinoHandler(QWidget):
    def __init__(self, port):
        super(ArduinoHandler, self).__init__()
        print(str(port))
        self.port = port
        self.serial = QSerialPort(
            port,
            baudRate = QSerialPort.Baud9600,
            readyRead = self.receive
        )
        self.serial.open(QIODevice.ReadWrite)

    @pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            # ~ self.output_te.append(text)
            rh = text.split(",")[0]
            t = text.split(",")[1]
            print(self.port +"\ttemp: "+ t +"\trh: "+rh) 
