# db2.py
import sqlite3

#연결객채(영구적으로 파일에 저장)
conn = sqlite3.connect(r"c:\work\test.db")  # 메모리 DB 생성
#커서 객체 생성
cur = conn.cursor()
cur.execute("select * from phonbook;")
#for row in cur:
#    print(row)
#cur.fetchall()
print(cur.fetchall())
conn.close()
