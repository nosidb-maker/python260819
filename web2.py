# web2.pu

#크롤링에 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup

#웹서버에 요청
import urllib.request

#정규표현식 검색: 특정 문자열 패턴
import re

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

#print("HTML 크기:", len(page))
#print("게시글 개수:", len(lst))
#print(page[:1000])

#선택한 블록을 주석 처리: ctrol + /
#<span class="subject_fixed" data-role="list-title-text" title="아이폰 12 프로 실버 128GB 정품 배터리 100% + 디스플레이 교체">
#							아이폰 12 프로 실버 128GB 정품 배터리 100% + 디스플레이 교체
#						</span>
