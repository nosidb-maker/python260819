# web2.pu

#크롤링에 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup

#웹서버에 요청
import urllib.request

#정규표현식 검색: 특정 문자열 패턴
import re

#파일에 저장
f = open("todayHumor.txt", "wt", encoding="utf-8")

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
#url = "https://www.clien.net/service/board/sold" 이 방식으로 할 때 404 권한 에러 발생
#일반 브라우저로 접속 시에는 header 정보가 포함되지만 python으로 할 때는 header 정보가 없어서 404 에러 발생한 것으로 보임
#url = "https://www.clien.net/service/board/sold"

hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}
#페이징 처리를 위한코드
for i in range(1, 11):
    url = "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=" + str(i)
    print(url)
    #웹브라우져 헤더 추가 
    req = urllib.request.Request(url, headers = hdr)
    data = urllib.request.urlopen(req).read()
    page = data.decode('utf-8', 'ignore')

    #웹서버에 요청
    soup = BeautifulSoup(page, "html.parser")
    #에러처리
    try:
        lst = soup.find_all("td", attrs={"class":"subject"})
        for tag in lst:
            #한번 더 검색을 한다
            title = tag.find("a").text.strip()
            # print(title)
            # f.write(title + "\n")   
            #검색
            if re.search("한국", title):
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
# <td class="subject">
# <a href="/board/view.php?table=bestofbest&amp;no=483650&amp;s_no=483650&amp;page=1" target="_top">깊이 잠든 밤. </a>
# <span class="list_memo_count_span"> [14]</span>  
# <span style="margin-left:4px;">
# <img src="//www.todayhumor.co.kr/board/images/list_icon_photo.gif" style="vertical-align:middle; margin-bottom:1px;"> 
# </span><img src="//www.todayhumor.co.kr/board/images/list_icon_pencil.gif?2" alt="창작글" style="margin-right:3px;top:2px;position:relative"> </td>
