from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
#이미지를 저장하기 위한 라이브러리 
from urllib.request import urlretrieve

def createFolder (name) :
    if os.path.isdir(f'./{name}') == False :
        os.mkdir(f'./{name}')
        print(f'{name} 폴더 생성 완료')
    else :
        print('이미 존재하는 폴더입니다.')


input_name = input("검색할 동물이름:")
driver = wb.Chrome()
driver.get(f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={input_name}")
#약간의 대기 시간 주기 
time.sleep(2) 
for i in range(2) : 
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
    time.sleep(2) 
print("스크롤 다운 완료")
img = driver.find_elements(By.CSS_SELECTOR, "._fe_image_tab_content_thumbnail_image") 

#이미지의 src속성값 가져오기 
src = [i.get_attribute('src') for i in img] 
srclst = []
#잘못된 주소를 가져온 src 데이터를 빼고 src_lst에 담기
for i in src : 
    if 'data:image' not in i :
            srclst.append(i)
#먼저 폴더를 생성 
createFolder(input_name) 
#.jpg 이미지 파일로 저장
for i in range(len(srclst)) : 
    urlretrieve(srclst[i], f'./{input_name}/{input_name}_{i+1}.jpg')
driver.close() # 브라우저 닫기
print(f'{input_name} 이미지 수집, 저장 작업 완료')



# <img src="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNTEyMDdfMjI2%2FMDAxNzY1MTE4MjI1NDA2.-wnvGaYPOL_HATDs0YYaik7fW7Wbv0NsY4LF6JFGO2Yg.VlGLIf_VtoxLJalhtNqSG28xlRbo8OKJ_CG-v-1z8BYg.JPEG%2FUntitled-3.jpg&amp;type=a340" class="_fe_image_tab_content_thumbnail_image" alt="강아지가 보는 세상은 조금 다르다? 강아지 시력" data-image-viewer-trigger="" data-image-viewer-img-id="image_sas:blog_63dea112f0d9db670d5ce76b2344fc03" data-thumb-width="340" data-thumb-height="510" data-is-min-width="true" data-is-max-width="false" width="144" height="216" style="position: relative; left: 50%; top: 0%; transform: translate(-50%, 0%); width: 122.66666666666666px; height: auto;" onerror="naver.common.handleImgError(this)">

