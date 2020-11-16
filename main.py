# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# Создать форму детального описания фильма
# Сделать настройки
# Сделать вход по паролю
# Расставить комментарии +

import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QMouseEvent
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QMessageBox, QAbstractItemView


from form.movie_add import MovieAddForm
from form.movie_detail import MovieDetailForm
from movie_database import MovieDatabase
from res_owner import ResourceOwner

# Инициалзиция базы данных
movieDatabase = MovieDatabase()


# Виджет одного объекта фильма
class MovieItemWidget(QWidget):
    # Сигнал для удаления виджета
    itemDeleted = pyqtSignal(QListWidgetItem)
    itemUpdated = pyqtSignal()

    def __init__(self, movie, item):
        super().__init__()
        # Сохранение ссылки на элемент виджета
        self._item = item
        self.movie = movie
        self.setupUi()

    def setupUi(self):

        self.setObjectName("Main_Form")
        self.resize(600, 300)
        self.setStyleSheet("color: #212121;")

        # Инициализация дочерних виджетов
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

        self.pushButton_favorite = QtWidgets.QPushButton(self)
        self.pushButton_favorite.setGeometry(self.width(), 200, 100, 50)
        self.pushButton_favorite.setText("В избранное")
        self.pushButton_favorite.setStyleSheet("margin: 8px")
        self.pushButton_favorite.clicked.connect(self.add_to_favorite)

        QtCore.QMetaObject.connectSlotsByName(self)

    def add_to_favorite(self):
        movieDatabase.add_movie_to_favorite(self.movie.uid)
        msg = QMessageBox(self)
        msg.setText("Добавлено")
        print(movieDatabase.get_favorite_movie())

    def removeItem(self):
        # Слот нажатия на кнопку удаления
        msg_warning = QMessageBox.question(self, "Предупреждение", "Вы уверены что хотите удалить фильм?",
                                           QMessageBox.Yes | QMessageBox.No)
        if msg_warning == QMessageBox.Yes:
            # Передача элемента в родительский виджет
            self.itemDeleted.emit(self._item)
            # Удаление фильма из базы данных
            movieDatabase.delete_movie(self.movie)

    # Событие двойного нажатия на элемент
    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self.detail = MovieDetailForm(self.movie, self)
            self.detail.show()

    def updateItem(self, movie):
        movieDatabase.update_movie(movie)
        self.itemUpdated.emit()


# Главное окно
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Словарь полей для фильтрации
        self.field_letters = {
            "Название": "title",
            "Жанр": "genre",
            "Рейтинг": "rating",
            "Дата выпуска": "year"
        }
        # Словарь типов фильмов для фильтрации
        self.type_letters = {
            "Фильм": "film",
            "Сериал": "serial"
        }
        self.current_mode = False
        self.setupUi()

    # Инициалзиция интерфейса
    def setupUi(self):
        self.setObjectName("Form")
        self.setGeometry(50, 50, 1280, 650)
        self.setFixedSize(1280, 650)
        self.setWindowTitle("Movie App")
        self.setWindowIcon(QIcon(ResourceOwner.icon))

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setEnabled(True)
        self.listWidget.setGeometry(QtCore.QRect(468, 90, 801, 541))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName("listWidget")

        self.label_type_view = QtWidgets.QLabel(self)
        self.label_type_view.setGeometry(468, 60, 801, 30)
        self.label_type_view.setAlignment(Qt.AlignCenter)
        self.label_type_view.setText("Кинотека")


        # Деление прямоугольника на 3 равные части
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(450 // 2 - 50, (661 // 3) // 2, 100, 100)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.open_add_form)

        self.pushButton_favorite = QtWidgets.QPushButton(self)
        self.pushButton_favorite.setObjectName("pushButton_3")
        self.pushButton_favorite.setGeometry(450 // 2 - 50, ((661 // 2) * 2) // 2, 100, 100)
        self.pushButton_favorite.clicked.connect(self.show_favorite_movie)

        self.pushButton_add_from_network = QtWidgets.QPushButton(self)
        self.pushButton_add_from_network.setObjectName("pushButton")
        self.pushButton_add_from_network.setGeometry(450 // 2 - 50, 661 - 150, 100, 100)
        self.pushButton_add_from_network.clicked.connect(self.add_from_network)

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
        # Иницилазция стилей
        self.setupStyleSheets()
        # Привязка данных к виджетам
        self.bind_data(None)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Movie App"))
        self.pushButton_2.setText(_translate("Form", "Добавить фильм"))
        self.pushButton_favorite.setText(_translate("Form", "Избранное"))
        self.pushButton_add_from_network.setText(_translate("Form", "Добавить из сети"))
        self.label_panel.setText(_translate("Form", "Панель управления"))
        self.comboBox_field.setItemText(0, "Название")
        self.comboBox_field.setItemText(1, "Жанр")
        self.comboBox_field.setItemText(2, "Рейтинг")
        self.comboBox_field.setItemText(3, "Дата выпуска")
        self.comboBox_type.setItemText(0, "Фильм")
        self.comboBox_type.setItemText(1, "Сериал")
        self.pushButton_search.setText("Найти")
        self.label_hint_type.setText("Тип")

    def add_from_network(self):
        movie = movieDatabase.get_movie_from_network(3423)
        self.add_movie_to_list(movie)

    def setupStyleSheets(self):
        self.label_filter.setStyleSheet("font-weight: bold; font-size: 15px")
        self.label_panel.setStyleSheet("border: 2px solid black;"
                                       " border-top: none;"
                                       " border-left: none;"
                                       "font-weight: bold;"
                                       "font-size: 15px")
        self.listWidget.setStyleSheet("#listWidget{border: 2px solid black; "
                                      " border-bottom: none;"
                                      " border-right: none;"
                                      "}")
        self.label_type_view.setStyleSheet(
            "border: 2px solid black; border-bottom: none;"
            "font-weight: bold; font-size: 15px; border-right: none")

    def open_add_form(self):
        # Форма добавления нового фильма
        self.ui = MovieAddForm(self)
        # Сокрытие родительского окна
        self.hide()
        self.ui.setupUi()
        self.ui.show()

    def show_favorite_movie(self):
        self.current_mode = not self.current_mode
        self.check_mode(self.current_mode)


    def check_mode(self, mode):
        if mode:
            self.pushButton_favorite.setText("Кинотека")
            self.bind_data(movieDatabase.get_favorite_movie())
            self.label_type_view.setText("Избранное")
        else:
            self.pushButton_favorite.setText("Избранное")
            self.bind_data(None)
            self.label_type_view.setText("Кинотека")

    def show_form(self):
        # Инкапсуляция события
        self.show()

    def removeItem(self, item):
        # Получить количество строк, соответствующих item
        row = self.listWidget.indexFromItem(item).row()
        # Удалить item
        item = self.listWidget.takeItem(row)
        # Удалить widget
        self.listWidget.removeItemWidget(item)
        del item

    def updateItem(self):
        self.bind_data(None)
        print("Апдейт")

    def bind_data(self, movie_list):
        # Очистить предыдущий список в целях предоствращения добавления одинаковых элементов
        self.listWidget.clear()
        # Если передается пустой список то мы берем фильмы из бд
        if movie_list is None:
            movie_list = movieDatabase.get_movie_list()
        # Перебираем фильмы и создаем виджеты
        self.set_data_to_widget(movie_list)

    def set_data_to_widget(self, movie_list):
        for i in movie_list:
            item = QListWidgetItem(self.listWidget)
            item.setSizeHint(QSize(600, 300))
            widget = MovieItemWidget(i, item)
            # Соединяем сигнал с родительской функцией удаления
            widget.itemDeleted.connect(self.removeItem)
            widget.itemUpdated.connect(self.updateItem)
            self.listWidget.setItemWidget(item, widget)

    def add_movie_to_list(self, movie):
        self.show_form()
        # Добавляем из MovieAddForm фильм в базу и обновляем список
        # Сильная привязанность + перебор всего переписка :((((((((((
        movieDatabase.add_movie(movie)
        self.bind_data(None)
        self.listWidget.scrollToBottom()

    # Функция фильтрации фильмов
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
        if current_field == "year":
            data = movieDatabase.search_by_year()
            self.bind_data(data)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
