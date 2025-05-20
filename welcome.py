from PySide6.QtWidgets import QApplication, QFormLayout,QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import api
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

		self.enter_email = QLineEdit()

		self.enter_password = QLineEdit()

		self.enter_password.setEchoMode(QLineEdit.Password)

		btn_submit = QPushButton("Войти")

		layout.addRow(title)
		layout.addRow("email",self.enter_email)
		layout.addRow("пароль",self.enter_password)
		layout.addRow(btn_submit)


		self.setLayout(layout)
		self.setFixedSize(300,200)

	def complete(self):
		return self.enter_email,self.enter_password

class RegisterWindow(QWidget):
	def __init__(self):
		super().__init__()
		layout = QFormLayout()

		title = QLabel("Регистрация")
		layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
		title.setStyleSheet(SUBTITLE_STYLE)

		self.enter_email = QLineEdit()

		self.enter_password = QLineEdit()
		self.enter_password.setEchoMode(QLineEdit.Password)

		self.confirm_password = QLineEdit()
		self.confirm_password.setEchoMode(QLineEdit.Password)

		self.btn_submit = QPushButton("Войти")

		layout.addRow(title)
		layout.addRow("email",self.enter_email)
		layout.addRow("пароль",self.enter_password)
		layout.addRow("подтвердите пароль",self.confirm_password)
		layout.addRow(self.btn_submit)


		self.setLayout(layout)
		self.setFixedSize(300,200)

	def complete(self):
		if self.enter_password.text() == self.confirm_password.text():
			return self.enter_email.text(),self.enter_password.text()
		else:
			if self.layout().count() <= 5:
				error_mag = QLabel("пароли не совпадают")
				error_mag.setStyleSheet("""
				color:red;
				""")
				self.layout().addWidget(error_mag)
			return None


test_app = QApplication()

client = api.Client(api.ServerConfig.addr)

register = RegisterWindow()
register.show()

def register_user():
	result = register.complete()
	if result is not None:
		print("starting")
		client.register_user(result[0],result[1])
		print("registred")
		register.close()


register.btn_submit.clicked.connect(register_user)

test_app.exec()

