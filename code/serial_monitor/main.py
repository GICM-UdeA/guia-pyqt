import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
from PyQt6.uic import loadUi
import serial
from serial.tools import list_ports

class Serial_Gui(QWidget):
    def __init__(self):
        super(Serial_Gui, self).__init__()
        loadUi("serial_ui.ui", self)

        self.red_led = QPixmap("led_red.png").scaled(20,20)
        self.green_led = QPixmap("led_green.png").scaled(20,20)

        self.connected = False
        self.led_indicator.setPixmap(self.red_led)

        self.serial_port = serial.Serial(timeout=3)
        self.serial_params = dict()
        self.COM_comboBox.addItems(["---", "refresh"] + [i.device for i in list_ports.comports()])
        self.BAUD_comboBox.addItems(["1200", "2400", "4800", "9600", "19200", "38400","57600", "115200"])

        self.COM_comboBox.currentIndexChanged.connect(self.set_COM_port)
        self.BAUD_comboBox.currentIndexChanged.connect(self.set_BAUD_rate)
        self.connect_disconnect_pushButton.clicked.connect(self.connect_disconnect_serial)
        self.clear_pushButton.clicked.connect(self.plainTextEdit.clear)
        
        self.counter=0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_serial)

    def set_COM_port(self):
        selectedItem = self.COM_comboBox.currentText()
        if selectedItem == "refresh":
            self.COM_comboBox.blockSignals(True)
            self.COM_comboBox.clear()
            self.COM_comboBox.addItems(["---", "refresh"] + [i.device for i in list_ports.comports()])
            self.COM_comboBox.blockSignals(False)
        else:
            self.serial_params["COM_PORT"] = selectedItem

        print(self.serial_params)

    def set_BAUD_rate(self):
        self.serial_params["BAUD_RATE"] = self.BAUD_comboBox.currentText()
        print(self.serial_params)

    def connect_disconnect_serial(self):
        self.connected = not self.connected
        if self.connected:
            self.led_indicator.setPixmap(self.green_led)
            self.timer.start(500)
        else:
            self.led_indicator.setPixmap(self.red_led)
            self.timer.stop()

    def read_serial(self):
        self.counter += 1
        self.plainTextEdit.appendPlainText(f"message {self.counter}: value {2}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    serial_gui = Serial_Gui()
    serial_gui.show()
    sys.exit(app.exec())