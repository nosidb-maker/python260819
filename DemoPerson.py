"""사람, 관리자, 직원 객체를 만들어 보는 아주 쉬운 상속 예제입니다.

파이썬에서 클래스는 사람을 만드는 '설계도'와 같습니다.
이 설계도로 사람을 만들면, 사람마다 번호와 이름을 가질 수 있습니다.
"""


class Person:
    """모든 사람에게 공통으로 필요한 정보를 담는 부모 클래스입니다.

    부모 클래스는 여러 종류의 사람이 함께 사용하는 기본 설계도입니다.
    여기에서는 모든 사람에게 필요한 id와 name을 준비합니다.
    """

    def __init__(self, id, name):
        """사람을 만들 때 번호와 이름을 받아서 보관합니다.

        self는 지금 만들고 있는 사람을 가리킵니다.
        self.id는 사람의 번호를 넣는 작은 상자이고,
        self.name은 사람의 이름을 넣는 작은 상자입니다.
        """
        self.id = id
        self.name = name

    def printInfo(self):
        """사람의 번호와 이름을 화면에 보여 줍니다."""
        print("Person(id: {0}, name: {1})".format(self.id, self.name))


class Manager(Person):
    """Person을 물려받아 만든 관리자 클래스입니다.

    Manager는 Person의 id와 name을 그대로 사용할 수 있습니다.
    여기에 관리자의 직책을 나타내는 title을 하나 더 가집니다.
    부모의 설계도를 물려받는 것을 '상속'이라고 합니다.
    """

    def __init__(self, id, name, title):
        """관리자의 번호, 이름, 직책을 준비합니다.

        super()는 부모 클래스인 Person을 부르는 도우미입니다.
        부모에게 id와 name을 먼저 맡기고,
        관리자가 새로 필요한 title은 여기에서 따로 보관합니다.
        """
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        """관리자의 번호, 이름, 직책을 화면에 보여 줍니다."""
        print("Manager(id: {0}, name: {1}, title: {2})".format(
            self.id, self.name, self.title
        ))


class Employee(Person):
    """Person을 물려받아 만든 직원 클래스입니다.

    Employee도 Person의 id와 name을 사용할 수 있습니다.
    여기에 직원이 잘하는 일을 나타내는 skill을 하나 더 가집니다.
    """

    def __init__(self, id, name, skill):
        """직원의 번호, 이름, 기술을 준비합니다.

        먼저 부모인 Person에게 id와 name을 전달합니다.
        그런 다음 직원만 사용하는 skill을 따로 보관합니다.
        """
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        """직원의 번호, 이름, 기술을 화면에 보여 줍니다."""
        print("Employee(id: {0}, name: {1}, skill: {2})".format(
            self.id, self.name, self.skill
        ))


"""서로 다른 종류의 사람 10명을 한 바구니에 담습니다.

Person 2명, Manager 4명, Employee 4명으로 모두 10명입니다.
각 사람은 자기 종류에 맞는 정보를 가지고 있습니다.
"""
people = [
    Person(1, "홍길동"),
    Person(2, "김민수"),
    Manager(3, "이영희", "개발팀장"),
    Manager(4, "박철수", "인사팀장"),
    Manager(5, "최수진", "기획팀장"),
    Manager(6, "정우성", "영업팀장"),
    Employee(7, "강하늘", "Python"),
    Employee(8, "윤서준", "Java"),
    Employee(9, "한지민", "디자인"),
    Employee(10, "오세훈", "데이터분석"),
]


"""바구니에서 사람을 한 명씩 꺼내 정보를 보여 줍니다.

for 문은 바구니 안에 있는 사람을 처음부터 끝까지 한 명씩 살펴봅니다.
person.printInfo()를 부르면 각 사람의 알맞은 printInfo()가 실행됩니다.
그래서 관리자는 직책을, 직원은 기술을 함께 보여 줄 수 있습니다.
"""
for person in people:
    person.printInfo()

p1=Person(3, "홍길동")
p1.printInfo()

