#s내부라이브러리 연습
import random

print(random.random())  # 0.0~1.0 사이의 랜덤한 실수
print(random.random())
#print(random.uniform(2.0, 5,0))  # 2.0~5.0 사이의 랜덤한 실수
print(random.choice(["가위", "바위", "보"]))  # 리스트에서 랜덤하게 하나 선택
print( [random.randrange(20) for i in range(10)])  # 0~19 사이의 랜덤한 정수 10개를 리스트로 생성
print( [random.randrange(20) for i in range(10)])  # 0~19 사이의 랜덤한 정수 10개를 리스트로 생성
print(random.sample(range(20), 10))  # 0~19 사이의 랜덤한 정수 10개를 리스트로 생성
print(random.sample(range(20), 10))  # 0~19 사이의 랜덤한 정수 10개를 리스트로 생성
#로또번호 만들기
print(random.sample(range(1,46), 5))  # 1~45 사이의 랜덤한 정수 5개를 리스트로 생성

#파일명 다루기
from os.path import *
#raw string notation: 암에 r을 붙이기
fileName = r"C:\python313\python.exe"
print( basename(fileName))  #파일명만 추출
print( abspath(fileName))  #절대경로 추출
print( abspath("python.exe"))  #절대경로 추출, 현재 디렉토리 기준

if exists(fileName):
    print("파일크기: {0}".format(getsize(fileName)))  #파일크기 추출
else:
    print("파일이 존재하지 않습니다.")


#운영체제의 정보
import os

print("운영체제:",os.name)
print("운영체제: {0}".format(os.name))
print("현재 작업 디렉토리: {0}".format(os.getcwd()))
print("환경변수:", os.environ)

#특정 폴더의 파일 리스트
import glob
print(glob.glob(r"c:\work\*.py"))  #c:\work 폴더의 모든 .py 파일 리스트
