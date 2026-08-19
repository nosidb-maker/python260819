#부모 클래스
class Person:
    # __init__ 메서드
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber

    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, self.phoneNumber))

class Student(Person):
    # person의 init를 상속받고 재정의
    def __init__(self, name, phoneNumber, subject, studentID):
        #탭으로 코딩
        #self.name = name
        #self.phoneNumber = phoneNumber
        super().__init__(name, phoneNumber)
        self.subject = subject
        self.studentID = studentID
    # person의 printInfo를 상속받고 재정의
    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, self.phoneNumber))
        print("Info(학과: {0}, 학번: {1})".format(self.subject, self.studentID))


p = Person("전우치", "010-222-1234")
s = Student("이순신", "010-111-1234", "컴공", "991122")
#print(p.__dict__)
#print(s.__dict__)
p.printInfo()
s.printInfo()  # student의 printinfo가 없으면 부모 클래스의 printinfo가 호출됨



