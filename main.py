from PySide6 import QtWidgets
from ui.ui import Ui_MainWindow
from qt_material import apply_stylesheet

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pyperclip


# 메인 ui 클래스
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.logic = MainLogic()

        # 로그인 관련 로직
        self.lineEdit_pw.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_pw.returnPressed.connect(self.login)
        self.pushButton_login.clicked.connect(self.login)

    def login(self):
        inputId = self.lineEdit_id.text()
        inputPw = self.lineEdit_pw.text()

        self.logic.login(inputId, inputPw)

# 메인 로직 클래스
class MainLogic:
    def login(self, inputId, inputPw):
        # 네이버 블로그 페이지 로딩
        self.driver = webdriver.Chrome()
        self.driver.get('https://section.blog.naver.com/BlogHome.naver')
        time.sleep(2)

        # 로그인 상태가 아니라면 네이버 로그인 화면으로 이동
        loginButton = self.driver.find_element(By.CLASS_NAME, "login_button")
        if loginButton is None:
            return
        else:
            loginButton.click()

        # 캡챠 우회 위해 복붙+딜레이 활용
        pyperclip.copy(inputId)
        self.driver.find_element(value="id").send_keys(Keys.CONTROL, 'v')
        time.sleep(2)

        pyperclip.copy(inputPw)
        self.driver.find_element(value="pw").send_keys(Keys.CONTROL, 'v')
        time.sleep(2)

        self.driver.find_element(value="log.login").click()


# Qt 애플리케이션 생성
app = QtWidgets.QApplication()
window = MainWindow()
apply_stylesheet(app, theme='dark_amber.xml')

# 애플리케이션 실행
window.show()
app.exec()
