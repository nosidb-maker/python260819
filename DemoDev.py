# DemoDev.py
# Developer라는 클래스를 정의하는데
# 멤버변수로 id, name, skill이 멤버변수로 있고 printinfo()라는 멤버메서드가 필요
# 각 라인별로 주석도 생성해줘.
class developer:
    # 생성자 메서드 정의
    def __init__(self, id, name, skill):
        self.id = id  # 개발자의 ID를 초기화
        self.name = name  # 개발자의 이름을 초기화
        self.skill = skill  # 개발자의 기술을 초기화

    # 개발자 정보를 출력하는 메서드 정의
    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Skill: {self.skill}")  # 개발자 정보 출력     

#인스턴스 생성
dev1 = developer(1, "Alice", "Python")
dev1.printInfo()  # 개발자 정보 출력



