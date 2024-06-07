from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
import mysql.connector
from mysql.connector import Error

class AgregarProductoWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Producto")
        self.setLayout(QVBoxLayout())

        self.nombre_edit = QLineEdit()
        self.descripcion_edit = QLineEdit()
        self.precio_edit = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_edit)
        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.descripcion_edit)
        layout.addWidget(QLabel("Precio:"))
        layout.addWidget(self.precio_edit)

        agregar_button = QPushButton("Agregar")
        agregar_button.clicked.connect(self.agregar_producto)
        layout.addWidget(agregar_button)

        self.setLayout(layout)

    def agregar_producto(self):
        nombre = self.nombre_edit.text()
        descripcion = self.descripcion_edit.text()
        precio = self.precio_edit.text()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='yauri',
                user='root',
                password=''
            )

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("INSERT INTO producto (nombre, descripcion, precio) VALUES (%s, %s, %s)",
                               (nombre, descripcion, precio))
                connection.commit()

        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                self.accept()