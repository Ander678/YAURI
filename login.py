import sys
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit, QPushButton, QMessageBox, QCheckBox, QVBoxLayout, QFormLayout, QHBoxLayout)
from registro import RegistrarUsuarioView
from main import MainWindow
from PyQt6.QtGui import QFont
import mysql.connector
from mysql.connector import Error
import bcrypt

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setGeometry(100, 100, 350, 250)
        self.setWindowTitle("Login")
        self.generar_formulario()
        self.show()

    def generar_formulario(self):
        self.is_logged = False

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.user_input = QLineEdit()
        self.user_input.setFont(QFont('Arial', 10))
        form_layout.addRow("Usuario:", self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setFont(QFont('Arial', 10))
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.password_input)

        layout.addLayout(form_layout)

        self.check_view_password = QCheckBox("Ver Contraseña")
        self.check_view_password.toggled.connect(self.mostrar_contrasena)
        layout.addWidget(self.check_view_password)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        register_button = QPushButton('Registrarte')
        register_button.clicked.connect(self.registrar_usuario)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def mostrar_contrasena(self, clicked):
        if clicked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def login(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='yauri',
                user='root',
                password=''
            )

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT password FROM usuarios WHERE username = %s",
                               (self.user_input.text(),))
                record = cursor.fetchone()

                if record and bcrypt.checkpw(self.password_input.text().encode('utf-8'), record[0].encode('utf-8')):
                    QMessageBox.information(self, "Inicio sesion", "Inicio de sesion exitoso",
                                            QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                    self.is_logged = True
                    self.close()
                    self.open_main_window()
                else:
                    QMessageBox.warning(self, "Error Message", "Credenciales incorrectas",
                                        QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)

        except Error as e:
            QMessageBox.warning(self, "Error Message", f"Error al conectar a la base de datos: {e}",
                                QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def registrar_usuario(self):
        self.new_user_form = RegistrarUsuarioView()
        self.new_user_form.show()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec())