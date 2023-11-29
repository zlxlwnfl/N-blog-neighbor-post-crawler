from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ui.ui import Ui_MainWindow
from qt_material import apply_stylesheet

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pyperclip


# 메인 ui 클래스
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logic = MainLogic()

        # 로그인 관련 로직
        self.lineEdit_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_pw.returnPressed.connect(self.login)
        self.pushButton_login.clicked.connect(self.login)

    def login(self):
        input_id = self.lineEdit_id.text()
        input_pw = self.lineEdit_pw.text()
        self.logic.login(input_id, input_pw)

    def closeEvent(self, event: QCloseEvent):
        result = QMessageBox.question(
            self,
            "종료 확인",
            "종료하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if result == QMessageBox.StandardButton.Yes:
            self.logic.window_close()
            event.accept()
        else:
            event.ignore()


# 메인 로직 클래스
class MainLogic:
    def __init__(self):
        self.driver = None

    def login(self, input_id, input_pw):
        # 네이버 블로그 페이지 로딩
        self.driver = webdriver.Chrome()
        self.driver.get('https://section.blog.naver.com/BlogHome.naver')
        time.sleep(2)

        # 로그인 상태가 아니라면 네이버 로그인 화면으로 이동
        login_button = self.driver.find_element(By.CLASS_NAME, "login_button")
        if login_button is None:
            return
        else:
            login_button.click()

        # 캡챠 우회 위해 복붙+딜레이 활용
        pyperclip.copy(input_id)
        self.driver.find_element(value="id").send_keys(Keys.CONTROL, 'v')
        time.sleep(2)

        pyperclip.copy(input_pw)
        self.driver.find_element(value="pw").send_keys(Keys.CONTROL, 'v')
        time.sleep(2)

        self.driver.find_element(value="log.login").click()

    def window_close(self):
        if self.driver is not None:
            self.driver.close()


# Qt 애플리케이션 생성
app = QApplication()
window = MainWindow()
apply_stylesheet(app, theme='dark_amber.xml')

# 애플리케이션 실행
window.show()
app.exec()
