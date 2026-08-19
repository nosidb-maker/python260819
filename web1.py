# web1.py
# 웹크롤링을 연습
# BeautifulSoup 모듈을 사용할 때 대체로 아래와 같이 선언하고 사용
from bs4 import BeautifulSoup

# 페이지를 로딩(rt : read text )
# 유니코드로 인코딩 해석(encoding="utf-8") --> 한국어, 중국어, 일본어 등 다양한 언어를 지원 (안깨짐)
# open 함수는 파일을 열고, read() 함수는 파일의 내용을 읽어온다.
# - 읽기 : rt, 쓰기 : wt, 첨부 : at (파일의 EOF 아래 내용 추가)
page = open("chap09_test.html", "rt", encoding="utf-8").read()

# 검색이 용이한 객체
soup = BeautifulSoup(page, "html.parser")
# 전체 페이지를 출력
#print(soup.prettify())

#<p> 태그를 전부 검색
#print(soup.find_all("p"))  # list 형식으로 데이터 출력

# 첫번째<p>만 검색
#print(soup.find("p"))  # 첫번째 <p>만 출력

# <p class="outer-text"> 만 검색
#print(soup.find_all("p", class_="outer-text"))  # list 형식으로 데이터 출력

#attrs 속성을 위 방식보다 많이 사용
#print(soup.find_all("p", attrs={"class":"outer-text"}))  # list 형식으로 필터링하여 데이터 출력

# 크롤링한 결과를 화면에만 출력
# 반복문: .text 속성으로 태그 안의 텍스트만 출력
#for item in soup.find_all("p"):
#    title = item.text.strip()  # strip() : 공백 제거
#    # 빈줄을 삭제
#    title = title.replace("\n", "")
#    print(title)

# 크롤링한 결과를 파일에 저장 + 화면에 출력
f = open("result.txt", "wt", encoding="utf-8")
# 반복문: .text 속성으로 태그 안의 텍스트만 출력
for item in soup.find_all("p"):
    title = item.text.strip()  # strip() : 공백 제거
    # 빈줄을 삭제
    title = title.replace("\n", "")
    print(title)
    f.write(title + "\n")

#파일을 닫기
f.close()   

