# 정규표현식.py
import re

for i in [1,2]:
    if i == 1:
        result1 = re.search("[0-9]*th", "35th")
        result2 = re.match("[0-9]*th", "35th")
    else:
        result1 = re.match("[0-9]*th", "  35th")
        result2 = re.match("[0-9]*th", " 35th")

    print(result1)
    print(result1.group())  # 35th
    print(result2)
    print(result2.group())  # 35th


