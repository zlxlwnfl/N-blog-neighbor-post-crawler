from PySide6.QtWidgets import *
from PySide6.QtGui import *

from ui.ui import Ui_MainWindow
from qt_material import apply_stylesheet

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

import time
import pyperclip


# 메인 ui 클래스
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logic = MainLogic()

        self.pushButton_search.setDisabled(True)
        self.pushButton_excelSave.setDisabled(True)

        # 로그인 관련 로직
        self.lineEdit_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_pw.returnPressed.connect(self.login)
        self.pushButton_login.clicked.connect(self.login)

    def login(self):
        input_id = self.lineEdit_id.text()
        input_pw = self.lineEdit_pw.text()

        result = self.logic.login(input_id, input_pw)
        if result is False:
            return

        self.pushButton_search.setEnabled(True)

        default_page_data = self.logic.find_default_page_data()
        self.lineEdit_startPage.setText(str(default_page_data[0]))
        self.lineEdit_endPage.setText(str(default_page_data[1]))

        self.comboBox_neighborGroup.addItems(self.logic.find_neighbor_group_list())

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
        self.web_browser: WebDriver = None

    def naver_blog_main_url(self) -> str:
        return 'https://section.blog.naver.com/BlogHome.naver'

    def login(self, input_id, input_pw) -> bool:
        # 네이버 블로그 페이지 로딩
        if self.web_browser is None:
            self.web_browser = webdriver.Chrome()
        self.web_browser.get(self.naver_blog_main_url())
        time.sleep(2)

        # 로그인 상태가 아니라면 네이버 로그인 화면으로 이동
        login_button = self.web_browser.find_element(By.CLASS_NAME, "login_button")
        if login_button is None:
            return True
        else:
            login_button.click()

        # 캡챠 우회 위해 복붙+딜레이 활용
        pyperclip.copy(input_id)
        self.web_browser.find_element(value="id").send_keys(Keys.CONTROL, 'v')
        time.sleep(2)

        pyperclip.copy(input_pw)
        self.web_browser.find_element(value="pw").send_keys(Keys.CONTROL, 'v')
        time.sleep(2)

        self.web_browser.find_element(value="log.login").click()
        time.sleep(2)
        if self.naver_blog_main_url() in self.web_browser.current_url:
            return True
        else:
            return False

    def find_default_page_data(self) -> []: # [start_page, end_page]
        page_navigation = self.web_browser.find_element(
            by=By.XPATH,
            value='//*[@id="content"]/section/div[3]/div',
        )
        if page_navigation is None:
            return [1, 1]

        pages = page_navigation.find_elements(
            by=By.TAG_NAME,
            value='span'
        )
        start_page = 1
        end_page = len(pages)

        return [start_page, end_page]

    def find_neighbor_group_list(self) -> []:
        self.web_browser.find_element(
            by=By.XPATH,
            value='//*[@id="content"]/section/div[1]/div/div/a/i',
        ).click()
        time.sleep(1)

        neighbor_group_elements_list = self.web_browser.find_element(
            by=By.XPATH,
            value='//*[@id="content"]/section/div[1]/div/div/div',
        ).find_elements(
            by=By.TAG_NAME,
            value='a',
        )
        neighbor_group_list = list(
            map(
                lambda x: x.text,
                neighbor_group_elements_list
            )
        )
        return neighbor_group_list

    def window_close(self):
        if self.web_browser is not None:
            self.web_browser.close()


# Qt 애플리케이션 생성
app = QApplication()
window = MainWindow()
apply_stylesheet(app, theme='light_blue.xml')

# 애플리케이션 실행
window.show()
app.exec()
