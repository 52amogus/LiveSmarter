from PySide6.QtWidgets import QApplication,QVBoxLayout,QWidget,QLabel,QPushButton
from PySide6.QtGui import QPixmap

class WelcomeScreenPage(QWidget):
	def __init__(self,title:str,text:str,image:QPixmap):
		super().__init__()
		layout = QVBoxLayout()
		picture = QLabel()
		picture.setPixmap(image)
		title = QLabel(title)
		text = QLabel(text)

		layout.addWidget(picture)
		layout.addWidget(title)
		layout.addWidget(text)

class WelcomeWindow(QWidget):
	def __init__(self):
		super().__init__()

