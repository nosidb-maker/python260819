# 문자열 연습.py

strA = "파이썬은 강력해"
strB = "python"
strC = """이 문자열은
다중 라인으로
저장합니다."""
strD="이 문자열도\n다중 라인\n저장"

print(strA)
print(len(strB))
print(strC)
print(strD)
#슬라이싱(인덱싱)
print(strB[0:3])
print(strB[:3])
print(strB[3:])
print(strB[-3:])

# list 연습
colors = ["red", "blue", "green"]
print(len(colors))
print(type(colors))
colors.append("white")
colors.insert(1, "pink")
print(colors)
colors.remove("blue")
print(colors)
print(colors.index("pink"))

# set 연습
# 중복 스스로 제거
a = {1,2,3,3}
b = {3,4,4,5}

print(a)
print(type(b))
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))

#tuple 연습
tp = (100, 200, 300)
print(len(tp))



#함수를 정의
#def 를 이용하여 함수를 정의
def times(a,b):
    return a+b, a*b

#함수를 호출
result = times(5, 6)
print(result)

print("id: %s, name: %s" % ("kim", "김유신"))

args = (3,4)
print(times(*args))
