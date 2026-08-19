# BankAccount.py

#은행의 계정을 표현한 클래스 
class BankAccount:
    def __init__(self, id, name, balance):
         # 클래스 내부에 이름을 숨기지 않은 경우 (하단의 account1.balance로 값 수정 가능)
#        self.id = id
#        self.name = name 
#        self.balance = balance 
#    def deposit(self, amount):
#        self.balance += amount 
#    def withdraw(self, amount):
#        self.balance -= amount
#    def __str__(self):
#        return "{0} , {1} , {2}".format(self.id, \
#            self.name, self.balance)

        # 클래스 내부에 이름을 숨김
        self.__id = id
        self.__name = name 
        self.__balance = balance 
    def deposit(self, amount):
        self.__balance += amount 
    def withdraw(self, amount):
        self.__balance -= amount
    def __str__(self):
        return "{0} , {1} , {2}".format(self.__id, \
            self.__name, self.__balance)


#인스턴스 객체를 생성
account1 = BankAccount(100, "전우치", 15000)
account1.withdraw(3000)

#외부에서 멤버변수에 접근 시 문제가 되는 경우
#account1.balance = 1500000000
print(account1)

#외부에서 접근
print(account1.__balance)
# <-- __balance 속성이 없다고 에러남.
# <-- private 하게 사용하기 위해서는 __를 붙여야 함

