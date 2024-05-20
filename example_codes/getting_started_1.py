import sys
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton

# Creamos una instancia de la aplicación
app = QApplication(sys.argv)

# Creamos una ventana principal (widget)
window = QWidget()
window.setGeometry(100, 100, 400, 100) # x, y, width, height
# Asignamos un título a la ventana
window.setWindowTitle("Mi primera GUI")

# Creamos un QLabel para mostrar un mensaje en la ventana
message = QLabel("<h1>¡Esta es mi primera GUI con PyQt!</h1>", parent=window)
message.move(10, 10) # x, y relativo a la ventana

# Creamos un QPushButton para monstrar en terminal un mensaje
button = QPushButton("Botón", parent=window)
button.move(150, 50)
button.clicked.connect(lambda: print("accionó el botón"))

# Mostramos la ventana
window.show()

# Ejecutamos el bucle de eventos de la aplicación
sys.exit(app.exec())
