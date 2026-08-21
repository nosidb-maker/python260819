import math
import re
import sys
from typing import List

import matplotlib

matplotlib.use("QtAgg")
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}

POSITIVE_KEYWORDS = [
    "맛있", "좋다", "만족", "추천", "재구매", "간편", "푸짐", "신선",
    "고소", "감칠", "든든", "깔끔", "진짜", "최고", "대박", "예술",
    "가성비", "풍성", "짱", "완벽", "달콤", "행복", "강추", "훌륭",
    "맛집", "기대", "만족스러", "감동", "쉬워", "편리", "좋아",
]
NEGATIVE_KEYWORDS = [
    "별로", "아쉽", "짜다", "비싸", "실망", "질기", "불만", "너무",
    "단점", "아쉬움", "짜증", "식감", "떨어지", "약하다", "무난",
    "부족", "냄새", "쓰다", "망", "후회", "질다", "덜하다", "딱히",
    "그냥", "속상", "불편", "쉽지", "실망스러", "산미", "짜증",
]


def ensure_korean_font():
    families = QFontDatabase().families()
    preferred = [
        "Malgun Gothic",
        "맑은 고딕",
        "Apple SD Gothic Neo",
        "Noto Sans CJK KR",
        "NanumGothic",
        "D2Coding",
        "Arial Unicode MS",
    ]
    for name in preferred:
        if name in families:
            return name
    return "Sans Serif"


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.text


def clean_comment(raw_text: str) -> str:
    text = raw_text.replace("\xa0", " ")
    text = re.sub(r"\!\[[^\]]*\]\([^\)]*\)", "", text)
    text = re.sub(r"\[[^\]]*\]\([^\)]*\)", "", text)
    text = re.sub(r"\d{4}\.\d{2}\.\d{2}.*?(도움돼요|추천|문의하기|상품 후기|리뷰)", "", text, flags=re.I)
    text = re.sub(r"\b도움돼요\s*\d+.*$", "", text)
    text = re.sub(r"\b\d+[가-힣A-Za-z]*\*\*\b", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\u200b", "")
    return text.strip(" -:.,")


def is_review_candidate(text: str) -> bool:
    text = clean_comment(text)
    if len(text) < 15:
        return False
    if re.search(r"\b(상품 후기|후기|리뷰|문의|배송|설명|상세정보|고객행복센터|공지|안내)\b", text):
        return False
    if not re.search(r"[가-힣]", text):
        return False
    return True


def extract_review_texts(html: str, max_count: int = 300) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    text_nodes: List[str] = []

    for element in soup.find_all(["p", "li", "div", "span"]):
        candidate = element.get_text(" ", strip=True)
        if is_review_candidate(candidate):
            cleaned = clean_comment(candidate)
            if cleaned and cleaned not in text_nodes:
                text_nodes.append(cleaned)

    if not text_nodes:
        return []

    return text_nodes[:max_count]


def classify_sentiment(text: str) -> str:
    lower = text.lower()
    pos_score = sum(lower.count(word.lower()) for word in POSITIVE_KEYWORDS)
    neg_score = sum(lower.count(word.lower()) for word in NEGATIVE_KEYWORDS)

    if pos_score > neg_score:
        return "긍정"
    if neg_score > pos_score:
        return "부정"
    return "중립"


def score_text(text: str) -> float:
    lower = text.lower()
    pos_score = sum(lower.count(word.lower()) for word in POSITIVE_KEYWORDS)
    neg_score = sum(lower.count(word.lower()) for word in NEGATIVE_KEYWORDS)
    total = pos_score + neg_score
    if total == 0:
        return 0.0
    return round((pos_score - neg_score) / total, 3)


def analyze_reviews(reviews: List[str]) -> pd.DataFrame:
    rows = []
    for review in reviews:
        label = classify_sentiment(review)
        if label == "중립":
            continue
        rows.append({
            "comment": review,
            "label": label,
            "score": score_text(review),
        })

    if not rows:
        raise ValueError("감성 분석할 리뷰가 없습니다.")

    df = pd.DataFrame(rows)
    df["score"] = df["score"].clip(-1.0, 1.0)
    return df


def create_sample_data() -> pd.DataFrame:
    base = [
        "맛있어서 다시 구매할 생각이에요. 진짜 만족하고 추천합니다.",
        "가격도 좋고 간편하게 만들 수 있어서 좋아요.",
        "푸짐하고 고소해서 가족들이 다 좋아했어요.",
        "국물이 감칠맛 있고 잘 어울려서 만족스럽습니다.",
        "배송도 빠르고 신선해요. 재구매 의사 있습니다.",
        "냄새도 좋고 양이 많은 편이라 좋았습니다.",
        "아쉬운 점은 없고 맛이 매우 좋았습니다.",
        "너무 만족스러워서 다음에도 구입할 예정입니다.",
        "입맛에 딱 맞고 간편하게 한 끼 해결하기 좋았어요.",
        "부대찌개 맛이 진하고 담백해서 추천합니다.",
        "짭짤하고 고소해서 밥이 계속 넘어가요.",
        "양도 넉넉하고 집에서 간편하게 먹기 좋아요.",
        "그냥 별로였어요. 기대보다 심심했습니다.",
        "가격 대비 만족도는 낮고 식감이 조금 아쉽습니다.",
        "너무 짜서 먹기가 힘들었고 재구매는 안 할 것 같습니다.",
        "양은 많은데 맛은 제 입맛에는 약했어요.",
        "국물이 약해서 아쉬웠고 전반적으로 평범했습니다.",
        "너무 느끼해서 부담스러웠고 비추입니다.",
        "재료가 부족한 느낌이 들고 소스가 약했어요.",
        "배달과는 달리 맛이 미흡하고 실망이 컸습니다.",
    ]
    rows = []
    for text in base:
        label = classify_sentiment(text)
        if label != "중립":
            rows.append({"comment": text, "label": label, "score": score_text(text)})
    return pd.DataFrame(rows)


def draw_donut_chart(canvas: FigureCanvas, df: pd.DataFrame):
    counts = {
        "긍정": int((df["label"] == "긍정").sum()),
        "부정": int((df["label"] == "부정").sum()),
        "중립": int((df["label"] == "중립").sum()),
    }
    total = max(sum(counts.values()), 1)
    values = [counts["긍정"], counts["부정"], counts["중립"]]
    colors = ["#2bb673", "#f05656", "#d0d3d8"]

    fig = canvas.figure
    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    ax.pie(
        values,
        labels=None,
        colors=colors,
        startangle=90,
        counterclock=True,
        wedgeprops={"width": 0.55, "edgecolor": "white", "linewidth": 1},
        autopct=lambda pct: f"{pct:.1f}%",
        pctdistance=0.6,
        textprops={"color": "#2a2a2a", "fontsize": 11, "fontweight": "bold"},
    )
    ax.text(0, 0, f"총 리뷰\n{total}", ha="center", va="center", fontsize=16, fontweight="bold")
    ax.set_title("감성 비율", fontsize=14)
    fig.tight_layout()
    canvas.draw()


def draw_histogram(canvas: FigureCanvas, df: pd.DataFrame):
    fig = canvas.figure
    fig.clear()
    ax = fig.add_subplot(111)

    scores = df["score"].tolist()
    bins = [-1.0, -0.6, -0.2, 0.2, 0.6, 1.0]
    ax.hist(scores, bins=bins, color="#66b3a6", edgecolor="black", alpha=0.9)
    ax.axvline(0.0, color="black", linestyle="--", linewidth=1.2)
    ax.set_title("감성 점수 분포", fontsize=14)
    ax.set_xlabel("감성 점수 (Score)")
    ax.set_ylabel("리뷰 수")
    fig.tight_layout()
    canvas.draw()


class ReviewAnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = create_sample_data()
        self.setup_ui()
        self.refresh_summary()
        self.populate_table()
        self.update_charts()

    def setup_ui(self):
        self.setWindowTitle("마켓컬리 상품 리뷰 & 감성 분석 데스크톱(PyQt6)")
        self.resize(1280, 860)
        self.setMinimumSize(1180, 760)

        font_name = ensure_korean_font()
        app_font = QFont(font_name, 10)
        QApplication.instance().setFont(app_font)

        self.setStyleSheet(
            """
            QMainWindow { background: #f2f2f2; color: #262626; }
            QWidget { background: #f5f5f5; }
            QLabel { color: #2a2a2a; }
            QLineEdit, QComboBox {
                background: white; border: 1px solid #d8d8d8; border-radius: 5px; padding: 7px 10px;
                min-height: 30px;
                font-size: 11pt;
            }
            QPushButton {
                border: 0; border-radius: 6px; background: #693D7A; color: white; font-weight: 700;
                min-height: 36px; padding: 0 16px;
            }
            QPushButton#secondary { background: #5b8def; }
            QPushButton#ghost { background: #f0f0f0; color: #333; border: 1px solid #d7d7d7; }
            QTableWidget {
                background: white; border: 1px solid #dfe1e5; border-radius: 8px; gridline-color: #ebeef2;
                font-size: 10.5pt;
            }
            QHeaderView::section {
                background: #f4f5f7; color: #3b3b3b; padding: 8px; font-weight: 600; border: none;
            }
            QProgressBar {
                border: 1px solid #d8d8d8; border-radius: 6px; background: #ebebeb; text-align: center;
            }
            QProgressBar::chunk { background: #6d2d80; }
            """
        )

        central = QWidget()
        self.setCentralWidget(central)

        main = QVBoxLayout(central)
        main.setContentsMargins(14, 10, 14, 10)
        main.setSpacing(12)

        topbar = QWidget()
        topbar.setObjectName("topbar")
        topbar.setStyleSheet("QWidget#topbar { background: #e7e7e7; border: 1px solid #d7d7d7; border-radius: 8px; }")
        top_layout = QHBoxLayout(topbar)
        top_layout.setContentsMargins(12, 8, 12, 8)

        title = QLabel("🧾 Kurly Review Analyzer")
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: #212121;")
        top_layout.addWidget(title)
        top_layout.addStretch()

        self.url_input = QLineEdit("https://www.kurly.com/goods/1001207466?collectionCode=sale231107")
        self.url_input.setFixedWidth(520)
        top_layout.addWidget(self.url_input)

        self.count_combo = QComboBox()
        self.count_combo.addItems(["50", "100", "200", "300", "500"])
        self.count_combo.setCurrentText("300")
        self.count_combo.setFixedWidth(90)
        top_layout.addWidget(self.count_combo)

        self.fetch_button = QPushButton("수집")
        self.fetch_button.setObjectName("secondary")
        self.fetch_button.clicked.connect(self.run_analysis)
        top_layout.addWidget(self.fetch_button)

        self.export_button = QPushButton("CSV 저장")
        self.export_button.setObjectName("ghost")
        self.export_button.clicked.connect(self.export_csv)
        top_layout.addWidget(self.export_button)

        self.save_chart_button = QPushButton("차트 저장")
        self.save_chart_button.setObjectName("ghost")
        self.save_chart_button.clicked.connect(self.save_chart)
        top_layout.addWidget(self.save_chart_button)

        main.addWidget(topbar)

        stat_bar = QWidget()
        stat_bar.setStyleSheet("QWidget { background: #f7f7f7; border: 1px solid #dfe2e5; border-radius: 10px; }")
        stat_layout = QGridLayout(stat_bar)
        stat_layout.setContentsMargins(14, 12, 14, 12)
        stat_layout.setHorizontalSpacing(14)
        stat_layout.setVerticalSpacing(10)

        self.stat_widgets = []
        labels = ["총 수집 리뷰", "긍정 의견", "부정 의견", "중립 의견", "감성 지수"]
        for i, label in enumerate(labels):
            card = QWidget()
            card.setStyleSheet("background: white; border: 1px solid #e2e2e2; border-radius: 8px;")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            title = QLabel(label)
            title.setStyleSheet("font-size: 12px; color: #666;")
            value = QLabel("0")
            value.setStyleSheet("font-size: 22px; font-weight: 700; color: #202020;")
            card_layout.addWidget(title)
            card_layout.addWidget(value)
            stat_layout.addWidget(card, 0, i)
            self.stat_widgets.append(value)

        main.addWidget(stat_bar)

        tabs = QWidget()
        tabs.setStyleSheet("QWidget { background: #f7f7f7; border: 1px solid #dfe2e5; border-radius: 10px; }")
        tabs_layout = QHBoxLayout(tabs)
        tabs_layout.setContentsMargins(16, 10, 16, 10)
        tabs_layout.addWidget(QPushButton("감성 요약"))
        tabs_layout.addWidget(QPushButton("주요 키워드 TOP 10"))
        tabs_layout.addStretch()
        main.addWidget(tabs)

        content = QSplitter(Qt.Orientation.Horizontal)
        content.setStyleSheet("QSplitter::handle { background: #dfe2e5; }")

        left_panel = QWidget()
        left_panel.setStyleSheet("background: white; border: 1px solid #dfe2e5; border-radius: 10px;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_title = QLabel("감성 비율")
        left_title.setStyleSheet("font-size: 14px; font-weight: 700;")
        left_layout.addWidget(left_title)
        self.donut_canvas = FigureCanvas(Figure(figsize=(5.0, 4.5), dpi=100))
        left_layout.addWidget(self.donut_canvas)

        right_panel = QWidget()
        right_panel.setStyleSheet("background: white; border: 1px solid #dfe2e5; border-radius: 10px;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_title = QLabel("감성 점수 분포")
        right_title.setStyleSheet("font-size: 14px; font-weight: 700;")
        right_layout.addWidget(right_title)
        self.hist_canvas = FigureCanvas(Figure(figsize=(6.0, 4.5), dpi=100))
        right_layout.addWidget(self.hist_canvas)

        content.addWidget(left_panel)
        content.addWidget(right_panel)
        content.setSizes([520, 620])
        main.addWidget(content)

        table_panel = QWidget()
        table_panel.setStyleSheet("background: white; border: 1px solid #dfe2e5; border-radius: 10px;")
        table_layout = QVBoxLayout(table_panel)
        table_layout.setContentsMargins(12, 12, 12, 12)
        table_top = QHBoxLayout()
        left_label = QLabel("감성 목록")
        left_label.setStyleSheet("font-weight: 700; font-size: 14px;")
        table_top.addWidget(left_label)
        table_top.addStretch()

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["전체", "긍정", "부정", "중립"])
        self.filter_combo.setFixedWidth(120)
        table_top.addWidget(self.filter_combo)
        table_layout.addLayout(table_top)

        self.review_table = QTableWidget(0, 5)
        self.review_table.setHorizontalHeaderLabels(["감성", "점수", "작성자", "작성일시", "리뷰 내용"])
        self.review_table.setColumnWidth(0, 90)
        self.review_table.setColumnWidth(1, 90)
        self.review_table.setColumnWidth(2, 100)
        self.review_table.setColumnWidth(3, 140)
        self.review_table.setAlternatingRowColors(True)
        self.review_table.setSelectionBehavior(self.review_table.SelectionBehavior.SelectRows)
        self.review_table.setEditTriggers(self.review_table.EditTrigger.NoEditTriggers)
        self.review_table.setWordWrap(True)
        self.review_table.verticalHeader().setVisible(False)
        self.review_table.verticalHeader().setDefaultSectionSize(60)
        self.review_table.horizontalHeader().setStretchLastSection(True)
        self.review_table.setStyleSheet(
            "QTableWidget::item { padding: 10px; color: #222; }"
            "QTableWidget::item:selected { background: #e9f0ff; color: #111; }"
        )
        table_layout.addWidget(self.review_table)
        main.addWidget(table_panel)

        status = QWidget()
        status.setStyleSheet("background: #f3f3f3; border: 1px solid #dfe2e5; border-radius: 8px;")
        status_layout = QHBoxLayout(status)
        status_layout.setContentsMargins(12, 8, 12, 8)

        self.status_label = QCheckBox("실시간 분석 상태")
        self.status_label.setChecked(True)
        self.status_label.setStyleSheet("font-size: 12px; color: #555;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(100)
        self.progress_bar.setFixedWidth(180)
        status_layout.addWidget(self.progress_bar)
        main.addWidget(status)

        self.filter_combo.currentIndexChanged.connect(self.apply_table_filter)

    def refresh_summary(self):
        total = len(self.df)
        positive = int((self.df["label"] == "긍정").sum())
        negative = int((self.df["label"] == "부정").sum())
        neutral = int((self.df["label"] == "중립").sum())
        mean_score = round(float(self.df["score"].mean()), 3) if not self.df.empty else 0.0

        values = [str(total), str(positive), str(negative), str(neutral), str(mean_score)]
        for widget, value in zip(self.stat_widgets, values):
            widget.setText(value)

    def update_charts(self):
        draw_donut_chart(self.donut_canvas, self.df)
        draw_histogram(self.hist_canvas, self.df)

    def _row_from_data(self, row):
        label = row["label"]
        score = f"{row['score']:.2f}"
        writer = "김**" if label == "긍정" else "박**"
        timestamp = "2026-08-21 16:52:25"
        comment = row["comment"]
        return label, score, writer, timestamp, comment

    def _set_row_height(self, row_index: int, comment: str):
        font = self.review_table.font()
        metrics = self.review_table.fontMetrics()
        max_chars_per_line = 50
        lines = max(1, len(comment) // max_chars_per_line + 1)
        if len(comment) > 80:
            lines = max(lines, 2)
        height = max(60, metrics.height() * lines + 18)
        self.review_table.setRowHeight(row_index, height)

    def _apply_item_style(self, row_index: int, label: str):
        item = self.review_table.item(row_index, 0)
        if not item:
            return
        if label == "긍정":
            item.setForeground(Qt.GlobalColor.darkGreen)
            item.setBackground(Qt.GlobalColor.lightGray)
        elif label == "부정":
            item.setForeground(Qt.GlobalColor.darkRed)
            item.setBackground(Qt.GlobalColor.lightGray)
        else:
            item.setForeground(Qt.GlobalColor.darkGray)
            item.setBackground(Qt.GlobalColor.lightGray)

    def populate_table(self):
        self.review_table.setRowCount(0)
        rows = self.df.sort_values("score", ascending=False).reset_index(drop=True)
        self.review_table.setRowCount(len(rows))

        for i, row in rows.iterrows():
            label, score, writer, timestamp, comment = self._row_from_data(row)
            if len(comment) > 180:
                comment = comment[:180] + "..."

            item_label = QTableWidgetItem(label)
            item_score = QTableWidgetItem(score)
            item_writer = QTableWidgetItem(writer)
            item_time = QTableWidgetItem(timestamp)
            item_comment = QTableWidgetItem(comment)

            item_label.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_score.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_writer.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_time.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_comment.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            item_comment.setFlags(item_comment.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.review_table.setItem(i, 0, item_label)
            self.review_table.setItem(i, 1, item_score)
            self.review_table.setItem(i, 2, item_writer)
            self.review_table.setItem(i, 3, item_time)
            self.review_table.setItem(i, 4, item_comment)
            self._apply_item_style(i, label)
            self._set_row_height(i, comment)

        self.review_table.resizeRowsToContents()
        for idx in range(self.review_table.rowCount()):
            if idx < self.review_table.rowCount():
                self.review_table.setRowHeight(idx, max(60, self.review_table.rowHeight(idx) + 18))

    def apply_table_filter(self):
        filter_text = self.filter_combo.currentText()
        self.review_table.setRowCount(0)
        rows = self.df.sort_values("score", ascending=False).reset_index(drop=True)
        if filter_text != "전체":
            rows = rows[rows["label"] == filter_text]

        self.review_table.setRowCount(len(rows))
        for i, row in rows.iterrows():
            label, score, writer, timestamp, comment = self._row_from_data(row)
            if len(comment) > 180:
                comment = comment[:180] + "..."

            item_label = QTableWidgetItem(label)
            item_score = QTableWidgetItem(score)
            item_writer = QTableWidgetItem(writer)
            item_time = QTableWidgetItem(timestamp)
            item_comment = QTableWidgetItem(comment)

            item_label.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_score.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_writer.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_time.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_comment.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            item_comment.setFlags(item_comment.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.review_table.setItem(i, 0, item_label)
            self.review_table.setItem(i, 1, item_score)
            self.review_table.setItem(i, 2, item_writer)
            self.review_table.setItem(i, 3, item_time)
            self.review_table.setItem(i, 4, item_comment)
            self._apply_item_style(i, label)
            self._set_row_height(i, comment)

        self.review_table.resizeRowsToContents()
        for i in range(self.review_table.rowCount()):
            self.review_table.setRowHeight(i, max(60, self.review_table.rowHeight(i) + 18))

    def run_analysis(self):
        url = self.url_input.text().strip()
        count = int(self.count_combo.currentText())
        if not url:
            QMessageBox.warning(self, "입력 오류", "상품 URL을 입력해 주세요.")
            return

        self.progress_bar.setValue(20)
        try:
            normalized_url = url if url.startswith("http") else "https://" + url
            html = fetch_html(normalized_url)
            reviews = extract_review_texts(html, max_count=count)
            if not reviews:
                raise ValueError("리뷰를 추출할 수 없습니다. 페이지 구조를 확인해 주세요.")
            self.df = analyze_reviews(reviews)
            self.status_label.setText(
                f"분석 완료 | 총 {len(reviews)}개 리뷰 수집, "
                f"긍정 {int((self.df['label'] == '긍정').sum())}개, "
                f"부정 {int((self.df['label'] == '부정').sum())}개"
            )
        except Exception as exc:
            self.df = create_sample_data()
            self.status_label.setText("네트워크 오류로 샘플 리뷰로 대체 분석했습니다.")
            QMessageBox.warning(
                self,
                "분석 경고",
                "리뷰를 불러오지 못해 샘플 데이터로 분석을 수행합니다.\n\n"
                f"원인: {exc}",
            )

        self.progress_bar.setValue(80)
        self.refresh_summary()
        self.update_charts()
        self.populate_table()
        self.progress_bar.setValue(100)

    def export_csv(self):
        path = "kurly_review_result.csv"
        self.df.to_csv(path, index=False, encoding="utf-8-sig")
        QMessageBox.information(self, "저장 완료", f"CSV 파일이 저장되었습니다.\n{path}")

    def save_chart(self):
        path = "kurly_review_chart.png"
        self.donut_canvas.figure.savefig(path, dpi=150, bbox_inches="tight")
        QMessageBox.information(self, "저장 완료", f"차트 이미지가 저장되었습니다.\n{path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app_font = QFont(ensure_korean_font(), 10)
    app.setFont(app_font)
    window = ReviewAnalysisWindow()
    window.show()
    sys.exit(app.exec())
