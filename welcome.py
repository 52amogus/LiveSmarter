from PySide6.QtWidgets import QApplication, QFormLayout,QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from data import TITLE_STYLE, SUBTITLE_STYLE

"""class WelcomeScreenPage(QWidget):
	def __init__(self,title:str,text:str,image:QPixmap):
		super().__init__()
		layout = QVBoxLayout()
		picture = QLabel()
		picture.setPixmap(image)
		title = QLabel(title)
		text = QLabel(text)

		layout.addWidget(picture)
		layout.addWidget(title)
		layout.addWidget(text)"""

class LoginWindow(QWidget):
	def __init__(self):
		super().__init__()
		layout = QFormLayout()

		title = QLabel("Добро пожаловать!")
		layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
		title.setStyleSheet(SUBTITLE_STYLE)

		enter_email = QLineEdit()

		enter_password = QLineEdit()

		enter_password.setEchoMode(QLineEdit.Password)

		btn_submit = QPushButton("Войти")

		layout.addRow(title)
		layout.addRow("email",enter_email)
		layout.addRow("пароль",enter_password)
		layout.addRow(btn_submit)


		self.setLayout(layout)
		self.setFixedSize(300,200)

class RegisterWindow(QWidget):
	def __init__(self):
		super().__init__()
		layout = QFormLayout()

		title = QLabel("Регистрация")
		layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
		title.setStyleSheet(SUBTITLE_STYLE)

		enter_email = QLineEdit()

		enter_password = QLineEdit()
		enter_password.setEchoMode(QLineEdit.Password)

		confirm_password = QLineEdit()
		confirm_password.setEchoMode(QLineEdit.Password)

		btn_submit = QPushButton("Войти")

		layout.addRow(title)
		layout.addRow("email",enter_email)
		layout.addRow("пароль",enter_password)
		layout.addRow("подтвердите пароль",confirm_password)
		layout.addRow(btn_submit)


		self.setLayout(layout)
		self.setFixedSize(300,200)

"""class WelcomeWindow(QWidget):
	def __init__(self):
		super().__init__()"""

test_app = QApplication()

win = RegisterWindow()
win.show()


test_app.exec()

