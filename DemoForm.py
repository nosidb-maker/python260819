# DemoForm.py
# Demoform.ui(화면단) + DemoForm.py(로직단)

import sys
#from PyQt6.QtWidgets import QApplication, QDiaglog
from PyQt6.QtWidgets import QApplication, QDialog 

from PyQt6 import uic

# 미리 준비한 .ui 파일을 로딩하여 화면을 띄우는 클래스 정의
from_class = uic.loadUiType("DemoForm.ui")[0]

# DemoForm 클래스 정의
class DemoForm(QDialog, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 화면단 초기화
        self.label.setText("Hello PyQt")  # label에 텍스트 설정

# 진입점을 체크해서 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성. 기본적으로 무조건 사용하는 매개변수 sys.argv는 명령행 인자를 처리하기 위해 사용
    demoWindows = DemoForm()  # DemoForm 객체 생성
    demoWindows.show()  # 화면에 띄우기
    sys.exit(app.exec())  # 이벤트 루프 실행
