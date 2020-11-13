# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QMouseEvent
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QMessageBox

from movie_app.form.movie_add import MovieAddForm
from movie_app.movie_database import MovieDatabase
from movie_app.network_service import NetworkService
from movie_app.res_owner import ResourceOwner

movieDatabase = MovieDatabase()
NetworkService().get_top_films()
class MovieItemWidget(QWidget):

    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, movie, item):
        super().__init__()
        self._item = item
        self.movie = movie
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Main_Form")
        self.resize(600, 300)
        self.setStyleSheet("color: #212121;")


        self.label_image = QtWidgets.QLabel(self)
        self.label_image.setGeometry(QtCore.QRect(10, 10, 131, 300))
        self.label_image.setObjectName("label_image")
        pixmap = QPixmap(self.movie.image_path)
        pixmap.scaledToWidth(131)
        pixmap.scaledToHeight(300)
        self.label_image.setPixmap(pixmap)

        self.label_title = QtWidgets.QLabel(self)
        self.label_title.setGeometry(QtCore.QRect(170, 10, self.width(), 21))
        self.label_title.setStyleSheet("font-weight: bold; font-size:  16px; color: black")
        self.label_title.setObjectName("label_title")
        self.label_title.setText(self.movie.title_ru)

        self.label_description = QtWidgets.QLabel(self)
        self.label_description.setGeometry(QtCore.QRect(170, 80, 231, 21))
        self.label_description.setObjectName("label_description")
        self.label_description.setText(self.movie.description)

        self.label_country = QtWidgets.QLabel(self)
        self.label_country.setGeometry(QtCore.QRect(170, 40, 221, 31))
        self.label_country.setObjectName("label_country")
        self.label_country.setText(f"<b>Страна</b> {self.movie.country}")

        self.label_created_date = QtWidgets.QLabel(self)
        self.label_created_date.setGeometry(QtCore.QRect(170, 110, 221, 21))
        self.label_created_date.setObjectName("label_created_date")
        self.label_created_date.setText(f"<b>Год выпуска</b> {self.movie.created_date}")

        self.label_rating = QtWidgets.QLabel(self)
        self.label_rating.setGeometry(QtCore.QRect(170, 140, 221, 21))
        self.label_rating.setObjectName("label_rating")
        self.label_rating.setText(f"{self.movie.rating}⭐")

        self.label_genres = QtWidgets.QLabel(self)
        self.label_genres.setGeometry(QtCore.QRect(170, 200, 221, 21))
        self.label_genres.setObjectName("label_genres")
        self.label_genres.setText(f"<b>Жанры</b> {self.movie.genres}")

        self.label_type = QtWidgets.QLabel(self)
        self.label_type.setGeometry(QtCore.QRect(170, 230, 221, 21))
        self.label_type.setText(self.movie.movie_type)
        self.label_type.setStyleSheet("font-weight: bold; font-size: 15px; marin: 8px")

        self.pushButton_delete = QtWidgets.QPushButton(self)
        self.pushButton_delete.setGeometry(self.width(), 250, 100, 50)
        self.pushButton_delete.setText("Удалить")
        self.pushButton_delete.setStyleSheet("margin: 8px")
        self.pushButton_delete.clicked.connect(self.removeItem)

        QtCore.QMetaObject.connectSlotsByName(self)


    def removeItem(self):
        msg_warning = QMessageBox.question(self, "Предупреждение", "Вы уверены что хотите удалить фильм?", QMessageBox.Yes|QMessageBox.No)
        if msg_warning == QMessageBox.Yes:
            self.itemDeleted.emit(self._item)
            movieDatabase.delete_movie(self.movie)


    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self.removeItem()



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.field_letters = {
            "Название": "title",
            "Жанр": "genre",
            "Рейтинг": "rating"
        }

        self.type_letters = {
            "Фильм": "film",
            "Сериал": "serial"
        }

    def setupUi(self):
        self.setObjectName("Form")
        self.setFixedSize(1280, 650)
        self.setWindowTitle("Movie App")
        self.setWindowIcon(QIcon(ResourceOwner.icon))

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setEnabled(True)
        self.listWidget.setGeometry(QtCore.QRect(468, 60, 801, 571))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName("listWidget")


        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(450 // 2 - 50, (661 // 3) // 2, 120, 120)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.open_add_form)

        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setGeometry(450 // 2 - 50, ((661 // 2) * 2) // 2, 120, 120)


        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(450 // 2 - 50, 661 - 150, 120, 120)


        self.label_panel = QtWidgets.QLabel(self)
        self.label_panel.setGeometry(QtCore.QRect(0, 2, 470, 60))
        self.label_panel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_panel.setAlignment(QtCore.Qt.AlignCenter)
        self.label_panel.setObjectName("label")

        self.label_filter = QtWidgets.QLabel(self)
        self.label_filter.setGeometry(QtCore.QRect(730, 0, 141, 25))
        self.label_filter.setObjectName("label_filter")

        self.lineEdit_query = QtWidgets.QLineEdit(self)
        self.lineEdit_query.setGeometry(QtCore.QRect(480, 30, 301, 25))
        self.lineEdit_query.setObjectName("lineEdit_query")
        self.lineEdit_query.setPlaceholderText("Введите запрос")
        # Событие о изменение текста
        # Создание вызова
        self.lineEdit_query.textChanged.connect(self.filter_movie)

        self.comboBox_field = QtWidgets.QComboBox(self)
        self.comboBox_field.setGeometry(QtCore.QRect(790, 30, 101, 25))
        self.comboBox_field.setObjectName("comboBox_field")
        self.comboBox_field.addItem("")
        self.comboBox_field.addItem("")
        self.comboBox_field.addItem("")

        self.comboBox_type = QtWidgets.QComboBox(self)
        self.comboBox_type.setGeometry(QtCore.QRect(930, 30, 69, 25))
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")

        self.label_hint_type = QtWidgets.QLabel(self)
        self.label_hint_type.setGeometry(QtCore.QRect(900, 30, 19, 25))
        self.label_hint_type.setStyleSheet("font-weight: bold")
        self.label_hint_type.setObjectName("label_hint_type")

        self.pushButton_search = QtWidgets.QPushButton(self)
        self.pushButton_search.setGeometry(QtCore.QRect(1010, 30, 70, 25))
        self.pushButton_search.setObjectName("pushbutton_search")
        self.pushButton_search.clicked.connect(self.filter_movie)

        self.retranslateUi()
        self.setupStyleSheets()
        self.bind_data(movieDatabase.get_movie_list())

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_2.setText(_translate("Form", "Добавить фильм"))
        self.pushButton_3.setText(_translate("Form", "Перейти в избраное"))
        self.pushButton.setText(_translate("Form", "Лол?)"))
        self.label_panel.setText(_translate("Form", "Панель управления"))
        self.comboBox_field.setItemText(0, "Название")
        self.comboBox_field.setItemText(1, "Жанр")
        self.comboBox_field.setItemText(2, "Рейтинг")
        self.comboBox_type.setItemText(0, "Фильм")
        self.comboBox_type.setItemText(1, "Сериал")
        self.pushButton_search.setText("Найти")
        self.label_hint_type.setText("Тип")

    def setupStyleSheets(self):
        self.label_filter.setStyleSheet("font-weight: bold; font-size: 15px")
        self.label_panel.setStyleSheet("border: 2px solid black;"
                                       " border-top: none;"
                                       " border-left: none;"
                                       "font-weight: bold;"
                                       "font-size: 15px")
        self.listWidget.setStyleSheet("#listWidget{border: 2px solid black; "
                                      " border-bottom: none;"
                                      " border-right: none}")

    def open_add_form(self):
        self.ui = MovieAddForm(self)
        self.hide()
        self.ui.setupUi()
        self.ui.show()

    def show_form(self):
        self.show()

    def removeItem(self, item):

        # Получить количество строк, соответствующих item
        row = self.listWidget.indexFromItem(item).row()
        # Удалить item
        item = self.listWidget.takeItem(row)
        # Удалить widget
        self.listWidget.removeItemWidget(item)
        del item

    def bind_data(self, movie_list):
        # Создать данные
        if movie_list is None:
            movie_list = movieDatabase.get_movie_list()

        self.listWidget.clear()
        for i in movie_list:
            item = QListWidgetItem(self.listWidget)
            item.setSizeHint(QSize(600, 300))
            widget = MovieItemWidget(i, item)
            widget.itemDeleted.connect(self.removeItem)
            self.listWidget.setItemWidget(item, widget)

    def add_movie_to_list(self, movie):
        movieDatabase.add_movie(movie)
        self.bind_data(None)
        self.listWidget.scrollToBottom()
        self.show()

    def filter_movie(self, query):
        current_field = self.field_letters[self.comboBox_field.currentText()]
        if query == "":
            self.bind_data(None)
        if current_field == "title":
            data = movieDatabase.search_by_title(query)
            self.bind_data(data)
        if current_field == "rating":
            data = movieDatabase.search_by_rating(True)
            self.bind_data(data)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = MainWindow()
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())
