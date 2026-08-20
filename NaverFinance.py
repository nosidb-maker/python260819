import time
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


BASE_URL = "https://finance.naver.com/sise/entryJongmok.naver"
INDEX_CODE = "KPI200"
TOTAL_PAGES = 20
OUTPUT_FILE = "kospi200.xlsx"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def make_page_url(page: int) -> str:
    """편입종목상위 페이지 URL을 생성합니다."""
    query = urlencode({"type": INDEX_CODE, "page": page})
    return f"{BASE_URL}?{query}"


def clean_text(tag) -> str:
    return " ".join(tag.stripped_strings)


def find_constituents_table(soup: BeautifulSoup):
    """편입종목상위 표를 찾습니다."""
    return soup.select_one("h4.top_tlt + table.type_1")


def parse_page(html: str, page: int) -> list[dict[str, str | int]]:
    soup = BeautifulSoup(html, "html.parser")
    table = find_constituents_table(soup)
    if table is None:
        raise ValueError(f"{page}페이지에서 편입종목상위 표를 찾지 못했습니다.")

    header_cells = table.select_one("tr").find_all("th")
    columns = [clean_text(cell) for cell in header_cells]
    rows = []

    for row in table.select("tr"):
        if row.select_one("td.ctg") is None:
            continue

        cells = row.find_all("td")
        values = [clean_text(cell) for cell in cells]
        if len(values) != len(columns):
            continue

        rows.append({"페이지": page, **dict(zip(columns, values))})

    return rows


def crawl_constituents(total_pages: int = TOTAL_PAGES) -> list[dict[str, str | int]]:
    """1페이지부터 total_pages페이지까지 편입종목상위 데이터를 수집합니다."""
    all_rows = []

    with requests.Session() as session:
        session.headers.update(HEADERS)

        for page in range(1, total_pages + 1):
            response = session.get(
                make_page_url(page),
                timeout=15,
            )
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "euc-kr"

            page_rows = parse_page(response.text, page)
            all_rows.extend(page_rows)
            print(f"{page:02d}/{total_pages}페이지 완료: {len(page_rows)}개")

            if page < total_pages:
                time.sleep(0.3)

    return all_rows


def save_to_excel(
    rows: list[dict[str, str | int]], filename: str = OUTPUT_FILE
) -> None:
    """크롤링 결과를 엑셀 파일로 저장합니다."""
    if not rows:
        raise ValueError("저장할 크롤링 결과가 없습니다.")

    columns = list(rows[0].keys())
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "KOSPI200 편입종목"
    worksheet.append(columns)

    for row in rows:
        worksheet.append([row[column] for column in columns])

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    workbook.save(filename)


if __name__ == "__main__":
    try:
        data = crawl_constituents()
        print(f"총 {len(data)}개의 편입종목 데이터를 수집했습니다.")
        save_to_excel(data)
        print(f"크롤링 결과를 {OUTPUT_FILE} 파일로 저장했습니다.")
    except requests.RequestException as error:
        print(f"네이버 금융 요청 중 오류가 발생했습니다: {error}")
    except ValueError as error:
        print(f"페이지 분석 중 오류가 발생했습니다: {error}")
