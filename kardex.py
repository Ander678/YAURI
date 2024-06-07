import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView,
    QPushButton, QHBoxLayout
)
from PyQt6.QtGui import QFont
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from agregarkar import AgregarKardexWindow

class KardexWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kardex Window")
        self.setGeometry(100, 100, 900, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.add_navigation_buttons()
        self.add_agregar_button()
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.show_kardex_table()
        self.add_sort_buttons()

    def add_sort_buttons(self):
        sort_layout_1 = QHBoxLayout()
        sort_layout_2 = QHBoxLayout()

        sort_kardex_id_button = QPushButton("Kardex ID (asc)")
        sort_kardex_id_button.clicked.connect(lambda: self.sort_table(column=0, reverse=False))
        sort_layout_1.addWidget(sort_kardex_id_button)

        sort_kardex_id_reverse_button = QPushButton("Kardex ID (desc)")
        sort_kardex_id_reverse_button.clicked.connect(lambda: self.sort_table(column=0, reverse=True))
        sort_layout_1.addWidget(sort_kardex_id_reverse_button)

        sort_product_id_button = QPushButton("Producto ID (asc)")
        sort_product_id_button.clicked.connect(lambda: self.sort_table(column=1, reverse=False))
        sort_layout_1.addWidget(sort_product_id_button)

        sort_product_id_reverse_button = QPushButton("Producto ID (desc)")
        sort_product_id_reverse_button.clicked.connect(lambda: self.sort_table(column=1, reverse=True))
        sort_layout_1.addWidget(sort_product_id_reverse_button)

        sort_date_button = QPushButton("Fecha (nueva-antigua)")
        sort_date_button.clicked.connect(lambda: self.sort_table(column=2, reverse=True, is_date=True))
        sort_layout_1.addWidget(sort_date_button)

        sort_date_reverse_button = QPushButton("Fecha (antigua-nueva)")
        sort_date_reverse_button.clicked.connect(lambda: self.sort_table(column=2, reverse=False, is_date=True))
        sort_layout_1.addWidget(sort_date_reverse_button)

        sort_entry_type_button = QPushButton("Tipo Movimiento (Entradas-Salidas)")
        sort_entry_type_button.clicked.connect(lambda: self.sort_table(column=3, reverse=False))
        sort_layout_1.addWidget(sort_entry_type_button)

        sort_entry_type_reverse_button = QPushButton("Tipo Movimiento (Salidas-Entradas)")
        sort_entry_type_reverse_button.clicked.connect(lambda: self.sort_table(column=3, reverse=True))
        sort_layout_1.addWidget(sort_entry_type_reverse_button)

        sort_price_button = QPushButton("Precio (asc)")
        sort_price_button.clicked.connect(lambda: self.sort_table(column=4, reverse=False))
        sort_layout_2.addWidget(sort_price_button)

        sort_price_reverse_button = QPushButton("Precio (desc)")
        sort_price_reverse_button.clicked.connect(lambda: self.sort_table(column=4, reverse=True))
        sort_layout_2.addWidget(sort_price_reverse_button)

        sort_client_id_button = QPushButton("Cliente ID (asc)")
        sort_client_id_button.clicked.connect(lambda: self.sort_table(column=5, reverse=False))
        sort_layout_2.addWidget(sort_client_id_button)

        sort_client_id_reverse_button = QPushButton("Cliente ID (desc)")
        sort_client_id_reverse_button.clicked.connect(lambda: self.sort_table(column=5, reverse=True))
        sort_layout_2.addWidget(sort_client_id_reverse_button)

        sort_supplier_id_button = QPushButton("Proveedor ID (asc)")
        sort_supplier_id_button.clicked.connect(lambda: self.sort_table(column=6, reverse=False))
        sort_layout_2.addWidget(sort_supplier_id_button)

        sort_supplier_id_reverse_button = QPushButton("Proveedor ID (desc)")
        sort_supplier_id_reverse_button.clicked.connect(lambda: self.sort_table(column=6, reverse=True))
        sort_layout_2.addWidget(sort_supplier_id_reverse_button)

        sort_quantity_button = QPushButton("Cantidad (asc)")
        sort_quantity_button.clicked.connect(lambda: self.sort_table(column=7, reverse=False))
        sort_layout_2.addWidget(sort_quantity_button)

        sort_quantity_reverse_button = QPushButton("Cantidad (desc)")
        sort_quantity_reverse_button.clicked.connect(lambda: self.sort_table(column=7, reverse=True))
        sort_layout_2.addWidget(sort_quantity_reverse_button)

        self.layout.addWidget(self.table_widget)
        self.layout.addLayout(sort_layout_1)
        self.layout.addLayout(sort_layout_2)

    def add_agregar_button(self):
        agregar_button = QPushButton("Agregar")
        agregar_button.clicked.connect(self.abrir_ventana_agregar)
        self.layout.addWidget(agregar_button)

    def abrir_ventana_agregar(self):
        self.agregar_window = AgregarKardexWindow()
        self.agregar_window.show()

    def sort_table(self, column, reverse, is_date=False):
        table_widget = self.table_widget
        records = []

        try:
            for row in range(table_widget.rowCount()):
                record = []
                for col in range(table_widget.columnCount()):
                    item = table_widget.item(row, col)
                    if item is not None:
                        record.append(item.text())
                    else:
                        record.append("")
                records.append(record)

            if is_date:
                sorted_records = sorted(records, key=lambda x: datetime.strptime(x[column], '%Y-%m-%d %H:%M:%S'), reverse=reverse)
            else:
                try:
                    sorted_records = sorted(records, key=lambda x: float(x[column]), reverse=reverse)
                except ValueError:
                    sorted_records = sorted(records, key=lambda x: x[column], reverse=reverse)

            table_widget.clearContents()

            for i, row_data in enumerate(sorted_records):
                for j, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(cell_data)
                    table_widget.setItem(i, j, item)
        except Exception as e:
            print(f"Error during sorting: {e}")

    def add_navigation_buttons(self):
        button_layout = QHBoxLayout()

        main_button = QPushButton("Inventario")
        main_button.clicked.connect(self.show_main)
        button_layout.addWidget(main_button)

        kardex_button = QPushButton("Kardex")
        kardex_button.clicked.connect(self.show_kardex)
        button_layout.addWidget(kardex_button)

        self.layout.addLayout(button_layout)

    def show_main(self):
        from main import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def show_kardex(self):
        self.show()

    def show_kardex_table(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='yauri',
                user='root',
                password=''
            )

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM kardex")
                records = cursor.fetchall()

                self.table_widget.setRowCount(len(records))
                self.table_widget.setColumnCount(8)
                self.table_widget.setHorizontalHeaderLabels(
                    ['ID', 'Producto ID', 'Fecha', 'Tipo Movimiento', 'Cantidad', 'Precio', 'Cliente ID',
                     'Proveedor ID'])

                for i, row in enumerate(records):
                    for j, cell in enumerate(row):
                        item = QTableWidgetItem(str(cell))
                        self.table_widget.setItem(i, j, item)

                header = self.table_widget.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

                self.layout.addWidget(self.table_widget)  # Agregar la tabla al layout

        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    kardex_window = KardexWindow()
    kardex_window.show()
    sys.exit(app.exec())