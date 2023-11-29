# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'N_blog_neighbor_post_crawler.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTableView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(693, 584)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_userAuth = QGroupBox(self.centralwidget)
        self.groupBox_userAuth.setObjectName(u"groupBox_userAuth")
        self.formLayout_2 = QFormLayout(self.groupBox_userAuth)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_id = QLabel(self.groupBox_userAuth)
        self.label_id.setObjectName(u"label_id")

        self.horizontalLayout.addWidget(self.label_id)

        self.lineEdit_id = QLineEdit(self.groupBox_userAuth)
        self.lineEdit_id.setObjectName(u"lineEdit_id")

        self.horizontalLayout.addWidget(self.lineEdit_id)

        self.label_pw = QLabel(self.groupBox_userAuth)
        self.label_pw.setObjectName(u"label_pw")

        self.horizontalLayout.addWidget(self.label_pw)

        self.lineEdit_pw = QLineEdit(self.groupBox_userAuth)
        self.lineEdit_pw.setObjectName(u"lineEdit_pw")

        self.horizontalLayout.addWidget(self.lineEdit_pw)

        self.pushButton_login = QPushButton(self.groupBox_userAuth)
        self.pushButton_login.setObjectName(u"pushButton_login")

        self.horizontalLayout.addWidget(self.pushButton_login)


        self.formLayout_2.setLayout(0, QFormLayout.LabelRole, self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox_userAuth)

        self.groupBox_filter = QGroupBox(self.centralwidget)
        self.groupBox_filter.setObjectName(u"groupBox_filter")
        self.formLayout = QFormLayout(self.groupBox_filter)
        self.formLayout.setObjectName(u"formLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_endPage = QLineEdit(self.groupBox_filter)
        self.lineEdit_endPage.setObjectName(u"lineEdit_endPage")

        self.gridLayout.addWidget(self.lineEdit_endPage, 0, 4, 1, 1)

        self.label_page = QLabel(self.groupBox_filter)
        self.label_page.setObjectName(u"label_page")

        self.gridLayout.addWidget(self.label_page, 0, 0, 1, 1)

        self.label_neighborGroup = QLabel(self.groupBox_filter)
        self.label_neighborGroup.setObjectName(u"label_neighborGroup")

        self.gridLayout.addWidget(self.label_neighborGroup, 1, 0, 1, 1)

        self.label_to = QLabel(self.groupBox_filter)
        self.label_to.setObjectName(u"label_to")

        self.gridLayout.addWidget(self.label_to, 0, 5, 1, 1)

        self.label_from = QLabel(self.groupBox_filter)
        self.label_from.setObjectName(u"label_from")

        self.gridLayout.addWidget(self.label_from, 0, 3, 1, 1)

        self.lineEdit_startPage = QLineEdit(self.groupBox_filter)
        self.lineEdit_startPage.setObjectName(u"lineEdit_startPage")

        self.gridLayout.addWidget(self.lineEdit_startPage, 0, 1, 1, 2)

        self.comboBox_neighborGroup = QComboBox(self.groupBox_filter)
        self.comboBox_neighborGroup.setObjectName(u"comboBox_neighborGroup")

        self.gridLayout.addWidget(self.comboBox_neighborGroup, 1, 1, 1, 2)


        self.formLayout.setLayout(0, QFormLayout.LabelRole, self.gridLayout)


        self.verticalLayout.addWidget(self.groupBox_filter)

        self.pushButton_search = QPushButton(self.centralwidget)
        self.pushButton_search.setObjectName(u"pushButton_search")

        self.verticalLayout.addWidget(self.pushButton_search)

        self.groupBox_result = QGroupBox(self.centralwidget)
        self.groupBox_result.setObjectName(u"groupBox_result")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_result)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableView_result = QTableView(self.groupBox_result)
        self.tableView_result.setObjectName(u"tableView_result")

        self.verticalLayout_3.addWidget(self.tableView_result)

        self.pushButton_excelSave = QPushButton(self.groupBox_result)
        self.pushButton_excelSave.setObjectName(u"pushButton_excelSave")

        self.verticalLayout_3.addWidget(self.pushButton_excelSave)


        self.verticalLayout.addWidget(self.groupBox_result)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 693, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"N\uc0ac \ube14\ub85c\uadf8 \uc774\uc6c3 \ud3ec\uc2a4\ud2b8 \ud06c\ub864\ub7ec", None))
        self.groupBox_userAuth.setTitle(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc790 \uc778\uc99d", None))
        self.label_id.setText(QCoreApplication.translate("MainWindow", u"ID", None))
        self.label_pw.setText(QCoreApplication.translate("MainWindow", u"PW", None))
        self.pushButton_login.setText(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8\uc778", None))
        self.groupBox_filter.setTitle(QCoreApplication.translate("MainWindow", u"\ud544\ud130", None))
        self.label_page.setText(QCoreApplication.translate("MainWindow", u"\ud398\uc774\uc9c0", None))
        self.label_neighborGroup.setText(QCoreApplication.translate("MainWindow", u"\uc774\uc6c3\uadf8\ub8f9     ", None))
        self.label_to.setText(QCoreApplication.translate("MainWindow", u"\uae4c\uc9c0", None))
        self.label_from.setText(QCoreApplication.translate("MainWindow", u"\uc5d0\uc11c", None))
        self.pushButton_search.setText(QCoreApplication.translate("MainWindow", u"\uac80\uc0c9 \uc2dc\uc791", None))
        self.groupBox_result.setTitle(QCoreApplication.translate("MainWindow", u"\uacb0\uacfc", None))
        self.pushButton_excelSave.setText(QCoreApplication.translate("MainWindow", u"\uc5d1\uc140 \uc800\uc7a5", None))
    # retranslateUi

