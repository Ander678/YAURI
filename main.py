import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QHeaderView, QPushButton, QHBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QFont
import mysql.connector
from mysql.connector import Error

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table_widget = QTableWidget()
        self.search_input = QLineEdit()  # Barra de búsqueda
        self.add_navigation_buttons()
        self.show_product_table()
        self.add_sort_buttons()
        self.add_search_bar()  # Agregar la barra de búsqueda

    def add_search_bar(self):
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_input)
        self.layout.addLayout(search_layout)

        self.search_input.textChanged.connect(self.filter_table)  # Conectar la señal textChanged

    def filter_table(self, text):
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 1)  # Columna del nombre del producto
            if item is not None:
                if text.lower() in item.text().lower():
                    self.table_widget.setRowHidden(row, False)
                else:
                    self.table_widget.setRowHidden(row, True)

    def add_sort_buttons(self):
        sort_layout = QHBoxLayout()

        sort_name_button = QPushButton("Nombre (A-Z)")
        sort_name_button.clicked.connect(lambda: self.sort_table(column=1, reverse=False))
        sort_layout.addWidget(sort_name_button)

        sort_name_reverse_button = QPushButton("Nombre (Z-A)")
        sort_name_reverse_button.clicked.connect(lambda: self.sort_table(column=1, reverse=True))
        sort_layout.addWidget(sort_name_reverse_button)

        sort_id_button = QPushButton("ID Producto (asc)")
        sort_id_button.clicked.connect(lambda: self.sort_table(column=0, reverse=False))
        sort_layout.addWidget(sort_id_button)

        sort_id_reverse_button = QPushButton("ID Producto (desc)")
        sort_id_reverse_button.clicked.connect(lambda: self.sort_table(column=0, reverse=True))
        sort_layout.addWidget(sort_id_reverse_button)

        sort_price_button = QPushButton("Precio (asc)")
        sort_price_button.clicked.connect(lambda: self.sort_table(column=3, reverse=False))
        sort_layout.addWidget(sort_price_button)

        sort_price_reverse_button = QPushButton("Precio (desc)")
        sort_price_reverse_button.clicked.connect(lambda: self.sort_table(column=3, reverse=True))
        sort_layout.addWidget(sort_price_reverse_button)

        sort_supplier_button = QPushButton("ID Proveedor (asc)")
        sort_supplier_button.clicked.connect(lambda: self.sort_table(column=4, reverse=False))
        sort_layout.addWidget(sort_supplier_button)

        sort_supplier_reverse_button = QPushButton("ID Proveedor (desc)")
        sort_supplier_reverse_button.clicked.connect(lambda: self.sort_table(column=4, reverse=True))
        sort_layout.addWidget(sort_supplier_reverse_button)

        self.layout.addLayout(sort_layout)

    def sort_table(self, column, reverse):
        records = []
        for row in range(self.table_widget.rowCount()):
            record = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item is not None:
                    record.append(item.text())
                else:
                    record.append("")
            records.append(record)

        sorted_records = sorted(records, key=lambda x: x[column], reverse=reverse)

        self.table_widget.clearContents()

        for i, row_data in enumerate(sorted_records):
            for j, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                self.table_widget.setItem(i, j, item)

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
        self.show()

    def show_kardex(self):
        from kardex import KardexWindow
        self.kardex_window = KardexWindow()
        self.kardex_window.show()
        self.close()

    def show_product_table(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='yauri',
                user='root',
                password=''
            )

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT producto_id, nombre, descripcion, precio, proveedor_id, cantidad FROM Producto")
                records = cursor.fetchall()

                self.table_widget.setRowCount(len(records))
                self.table_widget.setColumnCount(6)  # Aumenta el número de columnas
                self.table_widget.setHorizontalHeaderLabels(['ID', 'Nombre', 'Descripción', 'Precio', 'Proveedor ID',
                                                             'Cantidad'])  # Agrega el encabezado de la nueva columna

                for i, row in enumerate(records):
                    for j, cell in enumerate(row):
                        self.table_widget.setItem(i, j, QTableWidgetItem(str(cell)))

                # Make columns stretch to fill available space
                header = self.table_widget.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

                self.layout.addWidget(self.table_widget)

        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
