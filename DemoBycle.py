import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class BicycleProductWindow(QMainWindow):
    """자전거용품을 SQLite에 저장하고 관리하는 화면."""

    DB_PATH = "bicycle_products.db"

    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect(self.DB_PATH)
        self.create_table()
        self.setup_ui()
        self.load_products()

    def create_table(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS MyProduct (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price INTEGER NOT NULL CHECK (price >= 0)
            )
            """
        )
        self.connection.commit()

    def setup_ui(self):
        self.setWindowTitle("자전거용품 관리")
        self.resize(820, 620)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 26, 30, 28)
        main_layout.setSpacing(18)

        title = QLabel("자전거용품 관리")
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        subtitle = QLabel("RIDE READY  /  자전거 라이프를 위한 용품 데이터베이스")
        subtitle.setObjectName("subtitleLabel")
        main_layout.addWidget(subtitle)

        form_layout = QFormLayout()
        form_layout.setContentsMargins(20, 16, 20, 20)
        form_layout.setHorizontalSpacing(24)
        form_layout.setVerticalSpacing(12)
        self.id_edit = QLineEdit()
        self.id_edit.setObjectName("idEdit")
        self.id_edit.setPlaceholderText("자동 생성")
        self.id_edit.setReadOnly(True)
        self.name_edit = QLineEdit()
        self.name_edit.setObjectName("nameEdit")
        self.name_edit.setPlaceholderText("예: 자전거 헬멧")
        self.price_edit = QLineEdit()
        self.price_edit.setObjectName("priceEdit")
        self.price_edit.setPlaceholderText("예: 50000")
        id_label = QLabel("상품 ID")
        name_label = QLabel("상품명")
        price_label = QLabel("가격")
        for label in (id_label, name_label, price_label):
            label.setProperty("formLabel", True)
        form_layout.addRow(id_label, self.id_edit)
        form_layout.addRow(name_label, self.name_edit)
        form_layout.addRow(price_label, self.price_edit)
        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.input_button = QPushButton("입력")
        self.update_button = QPushButton("수정")
        self.delete_button = QPushButton("삭제")
        self.search_button = QPushButton("검색")
        self.all_button = QPushButton("전체보기")
        self.clear_button = QPushButton("입력 지우기")
        self.input_button.setObjectName("inputButton")
        self.update_button.setObjectName("updateButton")
        self.delete_button.setObjectName("deleteButton")
        self.search_button.setObjectName("searchButton")
        self.all_button.setObjectName("allButton")
        self.clear_button.setObjectName("clearButton")
        button_layout.addWidget(self.input_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.all_button)
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)

        self.table = QTableWidget(0, 3)
        self.table.setObjectName("productTable")
        self.table.setHorizontalHeaderLabels(["ID", "상품명", "가격"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.cellClicked.connect(self.select_product)
        main_layout.addWidget(self.table)

        self.input_button.clicked.connect(self.insert_product)
        self.update_button.clicked.connect(self.update_product)
        self.delete_button.clicked.connect(self.delete_product)
        self.search_button.clicked.connect(self.search_products)
        self.all_button.clicked.connect(self.load_products)
        self.clear_button.clicked.connect(self.clear_inputs)
        self.id_edit.returnPressed.connect(self.name_edit.setFocus)
        self.name_edit.returnPressed.connect(self.price_edit.setFocus)
        self.price_edit.returnPressed.connect(self.input_button.click)

        self.setStyleSheet(
            """
            QMainWindow {
                background: #0d1726;
            }
            #centralWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #101f33, stop: 0.58 #122a3b, stop: 1 #173c43
                );
            }
            #titleLabel {
                color: #f4fbf8;
                font-size: 29px;
                font-weight: 800;
                padding-top: 4px;
            }
            #subtitleLabel {
                color: #77d7c4;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1px;
                padding-bottom: 4px;
            }
            QFormLayout {
                background: rgba(10, 20, 34, 190);
                border: 1px solid #2d5260;
                border-radius: 14px;
            }
            QLabel[formLabel="true"] {
                color: #ffffff;
                font-size: 13px;
                font-weight: 700;
            }
            QLineEdit {
                min-height: 35px;
                padding: 0 12px;
                color: #eaf8f5;
                background: #172c3d;
                border: 1px solid #365b68;
                border-radius: 8px;
                selection-background-color: #32b49f;
            }
            QLineEdit:focus {
                border: 2px solid #5de0c3;
                background: #1a3545;
            }
            QLineEdit:read-only {
                color: #a7c2c3;
                background: #122638;
                border-color: #2b4e5a;
            }
            QLineEdit::placeholder {
                color: #718c98;
            }
            QPushButton {
                min-height: 38px;
                padding: 0 15px;
                color: #dffaf3;
                background: #214657;
                border: 1px solid #396a74;
                border-radius: 9px;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #2e6370;
                border-color: #6adbc7;
            }
            QPushButton:pressed {
                background: #173943;
            }
            #inputButton {
                color: #08231f;
                background: #57ddbd;
                border: none;
            }
            #inputButton:hover {
                background: #79ecd1;
            }
            #updateButton {
                color: #13251e;
                background: #b9e76d;
                border: none;
            }
            #updateButton:hover {
                background: #d2f48d;
            }
            #deleteButton {
                color: #fff4ed;
                background: #b95248;
                border: none;
            }
            #deleteButton:hover {
                background: #d96959;
            }
            #searchButton {
                background: #315e87;
                border-color: #4b87b3;
            }
            #allButton {
                background: #4d427d;
                border-color: #7465ae;
            }
            #clearButton {
                color: #c1d1d5;
                background: transparent;
                border-color: #49636b;
            }
            QTableWidget {
                color: #e4f1ef;
                background: rgba(12, 24, 39, 235);
                alternate-background-color: #172f3e;
                border: 1px solid #315866;
                border-radius: 12px;
                gridline-color: #294754;
                selection-background-color: #287f7a;
                selection-color: #ffffff;
                outline: none;
            }
            QHeaderView::section {
                min-height: 34px;
                color: #8de8d2;
                background: #183747;
                border: none;
                border-bottom: 2px solid #3abda7;
                font-weight: 800;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #203f4d;
            }
            QScrollBar:vertical {
                width: 10px;
                background: #102333;
                margin: 3px;
            }
            QScrollBar::handle:vertical {
                min-height: 35px;
                background: #347d7b;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
            """
        )

    def get_input_values(self):
        try:
            price = int(self.price_edit.text().strip())
        except ValueError:
            raise ValueError("가격은 숫자로 입력하세요.")

        name = self.name_edit.text().strip()
        if not name:
            raise ValueError("상품명을 입력하세요.")
        if price < 0:
            raise ValueError("가격은 0 이상이어야 합니다.")
        return name, price

    def get_selected_id(self):
        try:
            product_id = int(self.id_edit.text().strip())
            if product_id <= 0:
                raise ValueError
            return product_id
        except ValueError:
            raise ValueError("수정하거나 삭제할 상품을 목록에서 선택하세요.")

    def insert_product(self):
        try:
            name, price = self.get_input_values()
            self.connection.execute(
                "INSERT INTO MyProduct (name, price) VALUES (?, ?)",
                (name, price),
            )
            self.connection.commit()
            self.load_products()
            self.clear_inputs()
        except ValueError as error:
            self.show_error(str(error))
        except sqlite3.IntegrityError:
            self.show_error("같은 ID의 상품이 이미 있습니다.")

    def update_product(self):
        try:
            product_id = self.get_selected_id()
            name, price = self.get_input_values()
            cursor = self.connection.execute(
                "UPDATE MyProduct SET name = ?, price = ? WHERE id = ?",
                (name, price, product_id),
            )
            self.connection.commit()
            if cursor.rowcount == 0:
                self.show_error("수정할 상품을 찾을 수 없습니다.")
                return
            self.load_products()
            self.clear_inputs()
        except ValueError as error:
            self.show_error(str(error))

    def delete_product(self):
        try:
            product_id = self.get_selected_id()
        except ValueError:
            self.show_error("삭제할 상품을 목록에서 선택하세요.")
            return

        cursor = self.connection.execute("DELETE FROM MyProduct WHERE id = ?", (product_id,))
        self.connection.commit()
        if cursor.rowcount == 0:
            self.show_error("삭제할 상품을 찾을 수 없습니다.")
            return
        self.load_products()
        self.clear_inputs()

    def search_products(self):
        search_id = self.id_edit.text().strip()
        name = self.name_edit.text().strip()
        query = "SELECT id, name, price FROM MyProduct WHERE 1 = 1"
        parameters = []

        if search_id:
            parameters.append(int(search_id))
            query += " AND id = ?"
        if name:
            query += " AND name LIKE ?"
            parameters.append(f"%{name}%")
        query += " ORDER BY id"
        rows = self.connection.execute(query, parameters).fetchall()
        self.display_products(rows)

    def load_products(self):
        rows = self.connection.execute(
            "SELECT id, name, price FROM MyProduct ORDER BY id"
        ).fetchall()
        self.display_products(rows)

    def display_products(self, rows):
        self.table.setRowCount(0)
        for row_index, (product_id, name, price) in enumerate(rows):
            self.table.insertRow(row_index)
            values = (str(product_id), name, f"{price:,}")
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column_index in (0, 2):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_index, column_index, item)

    def select_product(self, row, _column):
        self.id_edit.setText(self.table.item(row, 0).text())
        self.name_edit.setText(self.table.item(row, 1).text())
        self.price_edit.setText(self.table.item(row, 2).text().replace(",", ""))

    def clear_inputs(self):
        self.id_edit.clear()
        self.name_edit.clear()
        self.price_edit.clear()
        self.table.clearSelection()

    def show_error(self, message):
        QMessageBox.warning(self, "확인", message)

    def closeEvent(self, event):
        self.connection.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BicycleProductWindow()
    window.show()
    sys.exit(app.exec())