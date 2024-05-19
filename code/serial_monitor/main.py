import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
from PyQt6.uic import loadUi
import serial
from serial.tools import list_ports

# Definición de la clase principal de la GUI
class Serial_Gui(QWidget):
    def __init__(self):
        super(Serial_Gui, self).__init__()
        
        # Carga de la interfaz desde un archivo .ui generado por Qt Designer
        loadUi("serial_ui.ui", self)
        
        # Carga y aplica los estilos CSS desde un archivo externo
        with open("styles.css") as f:
            self.setStyleSheet(f.read())

        # Carga las imágenes para los indicadores LED (rojo y verde) y las escala
        self.red_led = QPixmap("led_red.png").scaled(20, 20)
        self.green_led = QPixmap("led_green.png").scaled(20, 20)

        # Inicializa el estado de conexión y configura el indicador LED a rojo
        self.connected = False
        self.led_indicator.setPixmap(self.red_led)

        # Configuración del puerto serial con un timeout de 3 segundos
        self.serial_port = serial.Serial(timeout=3)
        self.serial_params = dict()

        # Pobla los ComboBox con los puertos COM disponibles y velocidades baud
        self.COM_comboBox.addItems(["---", "refresh"] + [i.device for i in list_ports.comports()])
        self.BAUD_comboBox.addItems(["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"])

        # Conexión de señales para manejar cambios en los ComboBox y botones
        self.COM_comboBox.currentIndexChanged.connect(self.set_COM_port)
        self.BAUD_comboBox.currentIndexChanged.connect(self.set_BAUD_rate)
        self.connect_disconnect_pushButton.clicked.connect(self.connect_disconnect_serial)
        self.clear_pushButton.clicked.connect(self.plainTextEdit.clear)
        
        # Inicializa un contador y un temporizador para la lectura serial
        self.counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_serial)

    # Maneja la selección del puerto COM
    def set_COM_port(self):
        selectedItem = self.COM_comboBox.currentText()
        if (selectedItem == "refresh"):  # Si se selecciona "refresh", actualiza la lista de puertos
            self.COM_comboBox.blockSignals(True)
            self.COM_comboBox.clear()
            self.COM_comboBox.addItems(["---", "refresh"] + [i.device for i in list_ports.comports()])
            self.COM_comboBox.blockSignals(False)
        else:  # Almacena el puerto seleccionado en los parámetros seriales
            self.serial_params["COM_PORT"] = selectedItem

        print(self.serial_params)

    # Maneja la selección de la velocidad baud
    def set_BAUD_rate(self):
        self.serial_params["BAUD_RATE"] = self.BAUD_comboBox.currentText()
        print(self.serial_params)

    # Conecta o desconecta el puerto serial
    def connect_disconnect_serial(self):
        self.connected = not self.connected
        if self.connected:  # Si se conecta, cambia el LED a verde y empieza el temporizador
            self.led_indicator.setPixmap(self.green_led)
            self.timer.start(500)
        else:  # Si se desconecta, cambia el LED a rojo y detiene el temporizador
            self.led_indicator.setPixmap(self.red_led)
            self.timer.stop()

    # Lee datos del puerto serial y los muestra en el widget de texto
    def read_serial(self):
        self.counter += 1
        self.plainTextEdit.appendPlainText(f"message {self.counter}: value {2}")

# Inicialización de la aplicación y ejecución de la interfaz gráfica
if __name__ == "__main__":
    app = QApplication(sys.argv)
    serial_gui = Serial_Gui()
    serial_gui.show()
    sys.exit(app.exec())
