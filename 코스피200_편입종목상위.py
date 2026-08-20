"""
네이버 금융 코스피200(KPI200) '편입종목상위' 크롤링
- 목록 페이지: https://finance.naver.com/sise/sise_index.naver?code=KPI200
- 편입종목상위 데이터는 위 페이지 내 iframe(entryJongmok.naver)에서 로드된다.
"""
import sys
import time

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

BASE_URL = "https://finance.naver.com/sise/entryJongmok.naver"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}


def get_soup(code: str, page: int) -> BeautifulSoup:
    """지정한 페이지의 HTML을 받아 BeautifulSoup 객체로 반환한다."""
    params = {"type": code, "page": page}
    response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    response.encoding = "euc-kr"  # 네이버 금융 페이지 인코딩
    return BeautifulSoup(response.text, "html.parser")


def parse_top_components(soup: BeautifulSoup) -> list[dict]:
    """'편입종목상위' 테이블 한 페이지 분량을 파싱해 리스트로 반환한다."""
    table = soup.select_one("table.type_1")
    if table is None:
        return []

    items = []
    for row in table.select("tr"):
        name_cell = row.select_one("td.ctg a")
        if not name_cell:
            continue  # 헤더/빈 구분 행 건너뜀

        cols = row.select("td")
        href = name_cell.get("href", "")
        stock_code = href.split("code=")[-1] if "code=" in href else ""

        items.append(
            {
                "종목코드": stock_code,
                "종목명": name_cell.get_text(strip=True),
                "현재가": cols[1].get_text(strip=True),
                "전일비": cols[2].get_text(" ", strip=True),
                "등락률": cols[3].get_text(strip=True),
                "거래량": cols[4].get_text(strip=True),
                "거래대금(백만)": cols[5].get_text(strip=True),
                "시가총액(억)": cols[6].get_text(strip=True),
            }
        )
    return items


def crawl_top_components(code: str = "KPI200", max_page: int = 20) -> list[dict]:
    """전체 페이지를 순회하며 편입종목상위 데이터를 모두 수집한다."""
    all_items = []
    for page in range(1, max_page + 1):
        soup = get_soup(code, page)
        items = parse_top_components(soup)
        if not items:
            break
        all_items.extend(items)
        time.sleep(0.3)  # 과도한 요청 방지
    return all_items


def save_to_excel(data: list[dict], file_path: str = "kospi200.xlsx") -> None:
    """크롤링 결과를 엑셀 파일로 저장한다."""
    if not data:
        raise ValueError("저장할 크롤링 결과가 없습니다.")

    wb = Workbook()
    ws = wb.active
    ws.title = "편입종목상위"

    headers = list(data[0].keys())
    ws.append(headers)
    for item in data:
        ws.append([item[header] for header in headers])

    wb.save(file_path)


class CrawlWorker(QObject):
    """백그라운드에서 네이버 금융 데이터를 수집한다."""

    progress = pyqtSignal(int, int)
    completed = pyqtSignal(list)
    failed = pyqtSignal(str)

    def __init__(self, code: str, max_page: int):
        super().__init__()
        self.code = code
        self.max_page = max_page

    def run(self):
        try:
            all_items = []
            for page in range(1, self.max_page + 1):
                soup = get_soup(self.code, page)
                items = parse_top_components(soup)
                if not items:
                    break
                all_items.extend(items)
                self.progress.emit(page, len(all_items))
                if page < self.max_page:
                    time.sleep(0.3)
            self.completed.emit(all_items)
        except (requests.RequestException, ValueError) as error:
            self.failed.emit(str(error))


class Kospi200Window(QMainWindow):
    """KOSPI200 편입종목상위 수집 및 엑셀 저장 화면."""

    def __init__(self):
        super().__init__()
        self.data = []
        self.thread = None
        self.worker = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("KOSPI200 편입종목상위")
        self.resize(1100, 680)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(14)

        title = QLabel("KOSPI200 편입종목상위")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        subtitle = QLabel("네이버 금융 데이터를 조회하고 엑셀 파일로 저장합니다.")
        subtitle.setObjectName("subtitleLabel")
        layout.addWidget(subtitle)

        form = QFormLayout()
        self.code_edit = QLineEdit("KPI200")
        self.page_spin = QSpinBox()
        self.page_spin.setRange(1, 100)
        self.page_spin.setValue(20)
        form.addRow("지수 코드", self.code_edit)
        form.addRow("최대 페이지", self.page_spin)
        layout.addLayout(form)

        button_layout = QHBoxLayout()
        self.crawl_button = QPushButton("데이터 조회")
        self.save_button = QPushButton("엑셀로 저장")
        self.save_button.setEnabled(False)
        button_layout.addWidget(self.crawl_button)
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.status_label = QLabel("조회할 조건을 입력한 뒤 데이터 조회를 누르세요.")
        layout.addWidget(self.status_label)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            [
                "종목코드",
                "종목명",
                "현재가",
                "전일비",
                "등락률",
                "거래량",
                "거래대금(백만)",
                "시가총액(억)",
            ]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table)

        self.crawl_button.clicked.connect(self.start_crawl)
        self.save_button.clicked.connect(self.save_excel)
        self.setStyleSheet(
            """
            QMainWindow, QWidget { background: #f4f1ea; color: #20272b; }
            #titleLabel { color: #183b3f; font-size: 26px; font-weight: 800; }
            #subtitleLabel { color: #607174; }
            QLineEdit, QSpinBox, QTableWidget { background: #fffdf8; border: 1px solid #c5cfca; border-radius: 6px; padding: 5px; }
            QPushButton { background: #176b68; color: white; border: 0; border-radius: 6px; padding: 9px 18px; font-weight: 700; }
            QPushButton:disabled { background: #aebbb8; }
            QHeaderView::section { background: #dce8e2; color: #183b3f; padding: 7px; font-weight: 700; }
            QTableWidget::item:selected { background: #b8d9cf; color: #183b3f; }
            """
        )

    def start_crawl(self):
        code = self.code_edit.text().strip().upper()
        if not code:
            QMessageBox.warning(self, "입력 확인", "지수 코드를 입력하세요.")
            return

        self.crawl_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.table.setRowCount(0)
        self.status_label.setText("데이터를 조회하는 중입니다...")

        self.thread = QThread(self)
        self.worker = CrawlWorker(code, self.page_spin.value())
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.completed.connect(self.crawl_completed)
        self.worker.failed.connect(self.crawl_failed)
        self.worker.completed.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.clear_worker)
        self.thread.start()

    def update_progress(self, page: int, count: int):
        self.status_label.setText(f"{page}페이지 조회 완료 / {count}개 수집")

    def crawl_completed(self, data: list):
        self.data = data
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(list(data[0].keys()) if data else [])
        self.table.setRowCount(len(data))
        for row_index, item in enumerate(data):
            for column_index, value in enumerate(item.values()):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(value)))
        self.crawl_button.setEnabled(True)
        self.save_button.setEnabled(bool(data))
        self.status_label.setText(f"총 {len(data)}개 종목을 수집했습니다.")

    def crawl_failed(self, message: str):
        self.crawl_button.setEnabled(True)
        self.status_label.setText("조회에 실패했습니다.")
        QMessageBox.critical(self, "조회 오류", message)

    def save_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "엑셀 파일 저장", "kospi200.xlsx", "Excel 파일 (*.xlsx)"
        )
        if not file_path:
            return
        try:
            save_to_excel(self.data, file_path)
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, "저장 오류", str(error))
            return
        self.status_label.setText(f"엑셀 파일로 저장했습니다: {file_path}")

    def clear_worker(self):
        self.worker.deleteLater()
        self.worker = None
        self.thread = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Kospi200Window()
    window.show()
    sys.exit(app.exec())
