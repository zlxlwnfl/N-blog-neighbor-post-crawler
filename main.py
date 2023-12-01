import urllib.parse

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from ui.ui import Ui_MainWindow
from qt_material import apply_stylesheet

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time
import pyperclip
import requests
from urllib.parse import urlparse, parse_qs, urlencode


# 메인 ui 클래스
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logic = MainLogic()

        self.init()

        # 로그인 관련 로직
        self.lineEdit_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_pw.returnPressed.connect(self.login)
        self.pushButton_login.clicked.connect(self.login)

        # 테이블뷰 헤더 설정
        table_top_header_labels = ['이웃명', '포스트 제목', '포스트 썸네일', '공감 개수', '댓글 개수', '포스트 url']
        self.model = QStandardItemModel(None, 0, len(table_top_header_labels))
        self.model.setHorizontalHeaderLabels(table_top_header_labels)

        self.tableView_result.setModel(self.model)

        header = self.tableView_result.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.pushButton_search.clicked.connect(self.search)

    def init(self):
        self.model = None

        self.pushButton_search.setDisabled(True)
        self.pushButton_excelSave.setDisabled(True)

    def login(self):
        input_id = self.lineEdit_id.text()
        input_pw = self.lineEdit_pw.text()

        result = self.logic.login(input_id, input_pw)
        if result is False:
            QMessageBox.warning(
                self,
                '로그인 오류',
                '정확한 아이디와 비밀번호를 적어주세요.',
                QMessageBox.StandardButton.Ok,
            )
            return

        self.pushButton_search.setEnabled(True)

        default_page_data = self.logic.find_default_page_data()
        self.lineEdit_startPage.setText(str(default_page_data[0]))
        self.lineEdit_endPage.setText(str(default_page_data[1]))

        self.comboBox_neighborGroup.addItems(self.logic.find_neighbor_group_list())

    def search(self):
        self.model.clear()
        self.pushButton_excelSave.setDisabled(True)

        # 페이지 설정
        start_page = int(self.lineEdit_startPage.text())
        end_page = int(self.lineEdit_endPage.text())

        if start_page > end_page:
            QMessageBox.warning(
                self,
                '경고',
                '시작 페이지가 끝 페이지보다 큰 값입니다.',
                QMessageBox.StandardButton.Ok
            )

        self.logic.close_floating_popup()

        # 이웃그룹 설정
        neighbor_group_id = self.logic.get_neighbor_group_id(self.comboBox_neighborGroup.currentIndex())

        data = self.logic.get_neighbor_post_data(start_page, end_page, neighbor_group_id)

        for row in range(len(data)):
            for column in range(len(data[0])):
                item = QStandardItem()

                if column == 2:
                    # 썸네일 가져오는 로직
                    if data[row][column] is not None:
                        pixmap = self.load_image_from_url(str(data[row][column]))
                        pixmap = pixmap.scaledToWidth(100)
                        item.setData(pixmap, Qt.ItemDataRole.DecorationRole)
                        # item.setSizeHint(pixmap.size())
                else:
                    item.setText(str(data[row][column]))

                self.model.setItem(row, column, item)

        self.pushButton_excelSave.setEnabled(True)

    def load_image_from_url(self, url: str):
        image = QImage()
        image.loadFromData(requests.get(url).content)
        pixmap = QPixmap.fromImage(image)
        return pixmap

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
        self.actions: ActionChains = None

        # 네이버 블로그 메인 url 쿼리 파싱
        naver_blog_main_url_query = urlparse(self.naver_blog_main_url()).query
        self.naver_blog_main_url_querys = parse_qs(naver_blog_main_url_query)

    def naver_blog_main_url(self) -> str:
        return 'https://section.blog.naver.com/BlogHome.naver?'

    def login(self, input_id: str, input_pw: str) -> bool:
        # 네이버 블로그 페이지 로딩
        if self.web_browser is None:
            self.web_browser = webdriver.Chrome()
            self.actions = ActionChains(self.web_browser)
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

    def find_default_page_data(self) -> []:  # [start_page, end_page]
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
        time.sleep(0.5)

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

    def get_neighbor_group_id(self, neighbor_group_index: int) -> int:
        self.set_neighbor_group(neighbor_group_index)
        current_url_query = urlparse(self.web_browser.current_url).query
        return int(parse_qs(current_url_query)['groupId'][0])

    def set_neighbor_group(self, neighbor_group_index: int):
        # 이웃 그룹 선택 콤보박스 닫기
        self.web_browser.find_element(
            by=By.CSS_SELECTOR,
            value='h3.title_heading',
        ).click()

        self.web_browser.find_element(
            by=By.XPATH,
            value='//*[@id="content"]/section/div[1]/div/div/a/i',
        ).click()
        time.sleep(0.5)

        self.web_browser.find_element(
            by=By.CSS_SELECTOR,
            value=f'a.item._buddy_dropdown_{neighbor_group_index}'
        ).click()
        time.sleep(0.5)

    def get_naver_blog_main_target_page_url(self, target_page: int, neighbor_group_id: int) -> str:
        self.naver_blog_main_url_querys['currentPage'] = [str(target_page)]
        self.naver_blog_main_url_querys['groupId'] = [str(neighbor_group_id)]
        return self.naver_blog_main_url() + urlencode(self.naver_blog_main_url_querys, encoding='UTF-8', doseq=True)

    def get_neighbor_post_data(self, start_page: int, end_page: int, neighbor_group_id: int) -> []:
        result_list = []

        for target_page in range(start_page, end_page+1):
            self.web_browser.get(self.get_naver_blog_main_target_page_url(target_page, neighbor_group_id))
            self.close_floating_popup()
            time.sleep(1)

            posts = None
            try:
                posts = self.web_browser.find_element(
                    by=By.CSS_SELECTOR,
                    value='div.list_post_article.list_post_article_comments'
                ).find_elements(
                    by=By.CLASS_NAME,
                    value='item_inner',
                )
            except NoSuchElementException:
                break

            for post in posts:
                post_neighbor_name = post.find_element(
                    by=By.CLASS_NAME,
                    value='name_author',
                ).text

                post_title = post.find_element(
                    by=By.CLASS_NAME,
                    value='title_post',
                ).text

                post_thumnail_image_url = None
                try:
                    post_thumnail_image_url = post.find_element(
                        by=By.CLASS_NAME,
                        value='img_post'
                    ).get_attribute('bg-image')
                except NoSuchElementException:
                    print("no thumnail image")

                post_heart_count = None
                try:
                    post_heart_count = post.find_element(
                        by=By.CSS_SELECTOR,
                        value='em.u_cnt._count',
                    ).text
                except NoSuchElementException:
                    print("no post_heart")
                    post_heart_count = 0

                post_comment_count = None
                try:
                    post_comment_count = post.find_element(
                        by=By.CSS_SELECTOR,
                        value='span.reply',
                    ).find_element(
                        by=By.TAG_NAME,
                        value='em',
                    ).text
                except NoSuchElementException:
                    print("no post_comment")
                    post_comment_count = 0

                post_url = post.find_element(
                    by=By.CLASS_NAME,
                    value='desc_inner'
                ).get_attribute('ng-href')

                result_list.append([
                    post_neighbor_name,
                    post_title,
                    post_thumnail_image_url,
                    post_heart_count,
                    post_comment_count,
                    post_url,
                ])

        print(result_list)
        return result_list

    def close_floating_popup(self):
        try:
            popup = self.web_browser.find_element(
                by=By.ID,
                value='floatingda_home'
            )
            self.actions.move_to_element(popup).perform()
            time.sleep(0.3)

            self.web_browser.find_element(
                by=By.XPATH,
                value='//*[@id="floatingda_home"]/div/button'
            ).click()
        except NoSuchElementException:
            pass

    def window_close(self):
        if self.web_browser is not None:
            self.web_browser.close()


# Qt 애플리케이션 생성
app = QApplication()
window = MainWindow()
apply_stylesheet(app, theme='dark_blue.xml')

# 애플리케이션 실행
window.show()
app.exec()
