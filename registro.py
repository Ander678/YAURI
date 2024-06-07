from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QFormLayout, QHBoxLayout)
import mysql.connector
from mysql.connector import Error
import bcrypt

class RegistrarUsuarioView(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()

    def generar_formulario(self):
        self.setGeometry(100, 100, 350, 250)
        self.setWindowTitle("Registration Window")

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.user_input = QLineEdit()
        self.user_input.setFont(QFont("Arial", 10))
        form_layout.addRow("Usuario:", self.user_input)

        self.password_1_input = QLineEdit()
        self.password_1_input.setFont(QFont("Arial", 10))
        self.password_1_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.password_1_input)

        self.password_2_input = QLineEdit()
        self.password_2_input.setFont(QFont("Arial", 10))
        self.password_2_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Repetir Password:", self.password_2_input)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        create_button = QPushButton("Crear")
        create_button.clicked.connect(self.crear_usuario)
        button_layout.addWidget(create_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.cancelar_creacion)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def cancelar_creacion(self):
        self.close()

    def crear_usuario(self):
        usuario = self.user_input.text()
        password1 = self.password_1_input.text()
        password2 = self.password_2_input.text()

        if password1 == '' or password2 == '' or usuario == '':
            QMessageBox.warning(self, "Error", "Por favor ingrese datos válidos",
                                QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
        elif password1 != password2:
            QMessageBox.warning(self, "Error", "Las contraseñas no son iguales",
                                QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
        else:
            try:
                connection = mysql.connector.connect(
                    host='localhost',
                    database='yauri',
                    user='root',
                    password=''
                )

                if connection.is_connected():
                    cursor = connection.cursor()
                    hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)",
                                   (usuario, hashed_password.decode('utf-8')))
                    connection.commit()
                    QMessageBox.information(self, 'Creación exitosa', 'Usuario creado correctamente',
                                            QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                    self.close()

            except Error as e:
                QMessageBox.warning(self, 'Error', f'Error al conectar a la base de datos: {e}',
                                    QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()