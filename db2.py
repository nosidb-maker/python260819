# db2.py
import sqlite3

#연결객채(영구적으로 파일에 저장)
conn = sqlite3.connect(r"c:\work\test.db")  # 메모리 DB 생성
#커서 객체 생성
cur = conn.cursor()
# 테이블 생성
#cur.execute("create table phonbook(name, text, phone text);")
#1건 입력
cur.execute("insert into phonbook (name, text, phone) values('홍길동', '서울시 강남구', '010-1234-5678');")
#입력 파라미터 처리
name = "전우치"
phone = "010-1234-5678"
cur.execute("insert into phonbook (name, phone) values(?,?);", (name, phone))

#d여러건 입력
datalist =[("이순신", "010-1111-2222"), ("강감찬", "010-3333-4444"), ("김유신", "010-5555-6666")]
cur.executemany("insert into phonbook (name, phone) values(?,?);", datalist)
#검색
cur.execute("select * from phonbook;")
for row in cur:
    print(row)

conn.commit();