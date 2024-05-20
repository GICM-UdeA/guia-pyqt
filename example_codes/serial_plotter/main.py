import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
from PyQt6.uic import loadUi
import serial
from serial.tools import list_ports
from numpy import random
from qt_material import apply_stylesheet
import resources

class Plotter_Gui(QWidget):
    def __init__(self):
        super(Plotter_Gui, self).__init__()
        loadUi("plotter_ui.ui", self)

        # se inicializa la gráfica
        self.init_plot()

        self.red_led = QPixmap("led_red.png").scaled(20, 20)
        self.green_led = QPixmap("led_green.png").scaled(20, 20)

        self.connected = False
        self.led_indicator.setPixmap(self.red_led)

        self.serial_port = serial.Serial(timeout=3)
        self.serial_params = dict()

        self.COM_comboBox.addItems(["---", "refresh"] + [i.device for i in list_ports.comports()])
        self.BAUD_comboBox.addItems(["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"])

        self.COM_comboBox.currentIndexChanged.connect(self.set_COM_port)
        self.BAUD_comboBox.currentIndexChanged.connect(self.set_BAUD_rate)
        self.connect_disconnect_pushButton.clicked.connect(self.connect_disconnect_serial)
        self.clear_pushButton.clicked.connect(self.reset_plot)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)



    def set_COM_port(self):
        selectedItem = self.COM_comboBox.currentText()
        if (selectedItem == "refresh"):
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


    # se inicializa la gráfica
    def init_plot(self):
        self.datax = [0]
        self.datay = [0]
        # se crea una referencia al Axes creado para poder actualizar los datos después
        self._plot_ref = self.plotter.canvas.axes.plot(self.datax, self.datay, label="Test data")[0]
        self.plotter.canvas.axes.set_title("Time series - test data")
        self.plotter.canvas.axes.set_xlabel("n")
        self.plotter.canvas.axes.set_ylabel("data")
        self.plotter.canvas.axes.grid(True, color="gray", linewidth=0.5)
        self.plotter.canvas.axes.legend(bbox_to_anchor=(0,0,1,1))

        self.plotter.canvas.draw()


    # Actualiza los datos de la gráfica
    def update_plot(self):
        self.datax.append(self.datax[-1] + 1)
        self.datay.append(random.rand() * 10)

        self._plot_ref.set_xdata(self.datax)
        self._plot_ref.set_ydata(self.datay)

        self.plotter.canvas.axes.dataLim.x1 = max(self.datax)
        self.plotter.canvas.axes.dataLim.y1 = max(self.datay)
        self.plotter.canvas.axes.autoscale_view()

        self.plotter.canvas.draw()

    # se reinia la gráfica
    def reset_plot(self):
        self.plotter.canvas.axes.cla()
        self.init_plot()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_teal.xml')
    Plotter_gui = Plotter_Gui()
    Plotter_gui.show()
    sys.exit(app.exec())
