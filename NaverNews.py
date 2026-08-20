import time
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


BASE_URL = "https://finance.naver.com/sise/sise_index.naver"
INDEX_CODE = "KPI200"
TOTAL_PAGES = 20
OUTPUT_FILE = "KPI200_편입종목상위.xlsx"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def make_page_url(page: int) -> str:
    query = urlencode({"code": INDEX_CODE, "page": page})
    return f"{BASE_URL}?{query}"


def clean_text(tag) -> str:
    return " ".join(tag.stripped_strings)


def find_constituents_table(soup: BeautifulSoup):
    for table in soup.find_all("table"):
        heading = table.find_previous(
            lambda tag: tag.name in {"h4", "h5"}
            and "편입종목상위" in clean_text(tag)
        )
        if heading:
            return table
    return None


def parse_constituents(html: str, page: int) -> list[dict[str, str | int]]:
    soup = BeautifulSoup(html, "html.parser")
    table = find_constituents_table(soup)
    if table is None:
        raise ValueError(f"{page}페이지에서 편입종목상위 표를 찾지 못했습니다.")

    rows = []
    for row in table.select("tr"):
        cells = row.find_all("td")
        values = [clean_text(cell) for cell in cells]
        if len(values) != 7 or not values[0]:
            continue

        rows.append(
            {
                "페이지": page,
                "종목별": values[0],
                "현재가": values[1],
                "전일비": values[2],
                "등락률": values[3],
                "거래량": values[4],
                "거래대금(백만)": values[5],
                "시가총액(억)": values[6],
            }
        )
    return rows


def crawl_constituents(total_pages: int = TOTAL_PAGES) -> list[dict[str, str | int]]:
    all_rows = []
    with requests.Session() as session:
        session.headers.update(HEADERS)
        for page in range(1, total_pages + 1):
            url = make_page_url(page)
            response = session.get(url, timeout=15)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "euc-kr"

            page_rows = parse_constituents(response.text, page)
            all_rows.extend(page_rows)
            print(f"{page:02d}/{total_pages}페이지 완료: {len(page_rows)}개")

            if page != total_pages:
                time.sleep(0.3)
    return all_rows


def save_to_excel(rows: list[dict[str, str | int]], filename: str = OUTPUT_FILE) -> None:
    columns = [
        "페이지",
        "종목별",
        "현재가",
        "전일비",
        "등락률",
        "거래량",
        "거래대금(백만)",
        "시가총액(억)",
    ]
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "편입종목상위"
    worksheet.append(columns)

    for row in rows:
        worksheet.append([row[column] for column in columns])

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    for column, width in {"A": 10, "B": 24, "C": 14, "D": 16, "E": 12, "F": 16, "G": 18, "H": 18}.items():
        worksheet.column_dimensions[column].width = width
    workbook.save(filename)


if __name__ == "__main__":
    try:
        rows = crawl_constituents()
        if not rows:
            print("편입종목상위 데이터를 찾지 못했습니다.")
        else:
            save_to_excel(rows)
            print(f"총 {len(rows)}개 종목을 {OUTPUT_FILE}에 저장했습니다.")
    except requests.RequestException as error:
        print(f"네이버 금융 요청 중 오류가 발생했습니다: {error}")
    except ValueError as error:
        print(f"페이지 분석 중 오류가 발생했습니다: {error}")