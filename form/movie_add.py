# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from movie import Movie
from movie_database import MovieDatabase
from res_owner import ResourceOwner

import random as rnd

class MovieAddForm(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.database = MovieDatabase()
        self.image_path = None
        self.parent = parent
        self.setStyleSheet("background-color: #3366CC; color: #FFFFFF; font-size: 13px; font-weight: bold")
        self.setWindowTitle("Добавить фильм")
        self.setWindowIcon(QIcon(ResourceOwner.icon))

    def setupUi(self):
        self.setObjectName("Form")
        self.setGeometry(200, 30, 640, 600)
        self.gridLayoutWidget = QtWidgets.QWidget(self)

        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 620, 530))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.lineEdit_country = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_country.setObjectName("lineEdit_creator")
        self.gridLayout.addWidget(self.lineEdit_country, 3, 1, 1, 1)

        self.label_description = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_description.setObjectName("label_description")
        self.label_description.setStyleSheet("margin: 5px; font-weight: bold; font-size: 13px")
        self.gridLayout.addWidget(self.label_description, 1, 0, 1, 1)

        self.label_image = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_image.setObjectName("label_image")
        self.label_image.setStyleSheet("margin: 5px; font-weight: bold; font-size: 13px")
        self.gridLayout.addWidget(self.label_image, 4, 0, 1, 1)

        self.lineEdit_title = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.gridLayout.addWidget(self.lineEdit_title, 0, 1, 1, 1)

        self.label_title = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_title.setObjectName("label_title")
        self.label_title.setStyleSheet("margin: 5px; font-weight: bold; font-size: 13px")
        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 1)

        self.pushButton_add_image = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_add_image.setObjectName("pushButton_add_image")
        self.pushButton_add_image.clicked.connect(self.on_click_get_image)
        self.pushButton_add_image.setStyleSheet("background-color: #757575; font-size: 15px; ")

        self.gridLayout.addWidget(self.pushButton_add_image, 4, 1, 1, 1)

        self.label_country = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_country.setObjectName("label_creator")
        self.label_country.setStyleSheet("margin: 5px")
        self.gridLayout.addWidget(self.label_country, 3, 0, 1, 1)

        self.label_year = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_year.setObjectName("label_year")
        self.label_year.setStyleSheet("margin: 5px")
        self.gridLayout.addWidget(self.label_year, 5, 0, 1, 1)

        self.lineEdit_year = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_year.setObjectName("lineEdit_year")
        self.gridLayout.addWidget(self.lineEdit_year, 5, 1, 1, 1)

        self.lineEdit_description = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_description.setObjectName("lineEdit_description")
        self.gridLayout.addWidget(self.lineEdit_description, 1, 1, 1, 1)

        self.lineEdit_genre = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_genre.setObjectName("lineEdit_genre")
        self.gridLayout.addWidget(self.lineEdit_genre, 2, 1, 1, 1)

        self.label_genre = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_genre.setObjectName("label_genre")
        self.label_genre.setStyleSheet("margin: 5px")
        self.gridLayout.addWidget(self.label_genre, 2, 0, 1, 1)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 480, 620, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_type = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_type.setObjectName("label_type")
        self.label_type.setStyleSheet("margin: 5px")
        self.horizontalLayout.addWidget(self.label_type)

        self.checkBox_film = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_film.setObjectName("checkBox_film")
        self.horizontalLayout.addWidget(self.checkBox_film)
        self.checkBox_serial = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_serial.setObjectName("checkBox_serial")
        self.horizontalLayout.addWidget(self.checkBox_serial)
        self.checkBox_anime = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_anime.setObjectName("checkBox_anime")
        self.horizontalLayout.addWidget(self.checkBox_anime)

        self.pushButton_make = QtWidgets.QPushButton(self)
        self.pushButton_make.setGeometry(QtCore.QRect(155, 551, 331, 41))
        self.pushButton_make.setObjectName("pushButton_make")
        self.pushButton_make.clicked.connect(self.on_click_add_movie)
        self.pushButton_make.setStyleSheet("background-color: #757575")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def on_click_get_image(self):
        owner = ResourceOwner()
        image_dialog = QFileDialog.getOpenFileName(self, "Выберите обложку", "", filter="*.jpg *.png")
        self.image_path = owner.copy_image_to_dir(image_dialog[0])

    def on_click_add_movie(self):
        if self.check_edit_is_empty():
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Ошибка")
            msgBox.setText("Заполните все поля!")
            msgBox.show()
            return

        title = self.lineEdit_title.text()
        created_date = self.lineEdit_year.text()
        country = self.lineEdit_country.text()
        # TODO: Add rating
        description = self.lineEdit_description.text()
        genres = self.lineEdit_genre.text()
        movie_type = "film"
        movie = Movie(title, created_date,
                      self.image_path, country, rnd.randint(0, 10), description, genres, movie_type)
        self.parent.add_movie_to_list(movie)
        self.close()

    def get_movie_type(self):
        film = ("film", self.checkBox_film.isChecked())
        serial = ("serial", self.checkBox_serial.isChecked())
        anime = ("anime", self.checkBox_anime.isChecked())

    def check_edit_is_empty(self):
        lineEdit_text_list = [not (self.lineEdit_title.text()), not (self.lineEdit_year.text()),
                              not (self.lineEdit_description.text()), not (self.lineEdit_country.text()),
                              not (self.lineEdit_genre.text())]
        print(lineEdit_text_list)
        print(lineEdit_text_list.count(True))
        if lineEdit_text_list.count(False) == 0:
            return True
        else:
            return False

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label_description.setText(_translate("Form", "Описание"))
        self.label_image.setText(_translate("Form", "Выбрать превью"))
        self.label_title.setText(_translate("Form", "Название"))
        self.pushButton_add_image.setText(_translate("Form", "Картинка"))
        self.label_country.setText(_translate("Form", "Страна"))
        self.label_year.setText(_translate("Form", "Год выпуска"))
        self.label_genre.setText(_translate("Form", "Жанр"))
        self.label_type.setText(_translate("Form", "Типа картины"))
        self.checkBox_film.setText(_translate("Form", "Фильм"))
        self.checkBox_serial.setText(_translate("Form", "Сериал"))
        self.checkBox_anime.setText(_translate("Form", "Аниме"))
        self.pushButton_make.setText(_translate("Form", "Создать"))
        self.lineEdit_title.setStyleSheet("background-color: #FFFFFF; color: black")
        self.lineEdit_country.setStyleSheet("background-color: #FFFFFF; color: black")
        self.lineEdit_genre.setStyleSheet("background-color: #FFFFFF; color: black")
        self.lineEdit_description.setStyleSheet("background-color: #FFFFFF; color: black")
        self.lineEdit_year.setStyleSheet("background-color: #FFFFFF; color: black")
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        msg = QMessageBox.question(self, "Предупреждение", "Вы уверены что хотите выйти?", QMessageBox.Ok, QMessageBox.No)
        if msg == QMessageBox.Ok:
            self.parent.show()
            a0.accept()
        else:
            a0.ignore()


