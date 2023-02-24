from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, QIODevice
from PyQt5.QtSerialPort import QSerialPort
import serial


class ArduinoHandler(QWidget):
    def __init__(self, port):
        super(ArduinoHandler, self).__init__()        
        self.temp = 0
        self.rh = 0
        self.port = port
        self.serial = QSerialPort(
            port,
            baudRate = QSerialPort.Baud9600,
            readyRead = self.receive
        )
        self.serial.open(QIODevice.ReadWrite)
        
    def get_data(self):
        return self.rh, self.temp

    @pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            try:
                text = self.serial.readLine().data().decode()
                text = text.rstrip('\r\n')
                self.rh = text.split(",")[0]
                self.temp = text.split(",")[1]
                
                # ~ print(self.port +"\ttemp: "+ self.temp +"\trh: " + self.rh) 
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
            except:
                print("Other error")
