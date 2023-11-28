from PySide6 import QtWidgets
from ui.ui import Ui_MainWindow
from qt_material import apply_stylesheet


# ui 클래스 상속
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

# Qt 애플리케이션 생성
app = QtWidgets.QApplication()
window = MainWindow()
apply_stylesheet(app, theme='dark_amber.xml')

# 애플리케이션 실행
window.show()
app.exec_()
