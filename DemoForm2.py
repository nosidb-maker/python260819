# DemoForm2.py
# Demoform2.ui(화면단) + DemoForm2.py(로직단)

import sys
#from PyQt6.QtWidgets import QApplication, QDiaglog
from PyQt6.QtWidgets import QApplication, QMainWindow 

from PyQt6 import uic
from bs4 import BeautifulSoup #크롤링에 필요한 라이브러리 불러오기
import urllib.request #웹서버에 요청
import re                     #정규표현식 검색: 특정 문자열 패턴

# 미리 준비한 .ui 파일을 로딩하여 화면을 띄우는 클래스 정의
from_class = uic.loadUiType("DemoForm2.ui")[0]

# DemoForm 클래스 정의
class DemoForm(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 화면단 초기화
    def firstClick(self):
        #파일에 저장
        f = open("clien.txt", "wt", encoding="utf-8")

        #User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
        #url = "https://www.clien.net/service/board/sold" 이 방식으로 할 때 404 권한 에러 발생
        #일반 브라우저로 접속 시에는 header 정보가 포함되지만 python으로 할 때는 header 정보가 없어서 404 에러 발생한 것으로 보임
        #url = "https://www.clien.net/service/board/sold"

        hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}
        #페이징 처리를 위한코드
        for i in range(0, 10):
            url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(i)
            print(url)
            #웹브라우져 헤더 추가 
            req = urllib.request.Request(url, headers = hdr)
            data = urllib.request.urlopen(req).read()
            page = data.decode('utf-8', 'ignore')

            #웹서버에 요청
            soup = BeautifulSoup(page, "html.parser")
            #에러처리
            try:
                lst = soup.find_all("span", attrs={"data-role":"list-title-text"})
                for tag in lst:
                    title = tag.text.strip()
                    #검색
                    if re.search("아이패드", title):
                        print(title)
                        f.write(title + "\n")
            except:
                pass    

        #파일을 닫기
        f.close()
        self.label.setText("중고장터 크롤링 완료")  # label에 첫번째 버튼 클릭 문자열 출력  
    def secondClick(self):
        self.label.setText("두번째 버튼 클릭")  
    def thirdClick(self):
        self.label.setText("세번째 버튼 클릭")

# 진입점을 체크해서 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성. 기본적으로 무조건 사용하는 매개변수 sys.argv는 명령행 인자를 처리하기 위해 사용
    demoWindows = DemoForm()  # DemoForm 객체 생성
    demoWindows.show()  # 화면에 띄우기
    sys.exit(app.exec())  # 이벤트 루프 실행
