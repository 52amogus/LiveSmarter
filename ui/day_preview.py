from PySide6.QtWidgets import QWidget,QLabel,QPushButton,QVBoxLayout,QHBoxLayout
from data import *
from model import load_all
from datetime import date
from .eventlist import EventList
from .new_event import NewEventWindow
from localization import word


def format_date(date1: date):
	return f"{date1.day} {word("months2")[date1.month - 1]} {date1.year}"

class DayPreview(QWidget):
	def __init__(self,day:date,separate=False):
		super().__init__()
		new_window = NewEventWindow(
			default_month=day.month,
			default_year=day.year
		)

		self.eventlist = EventList(load_all(day),day)

		def show_new():
			new_window.show()

		def create_new():
			item = new_window.create_new(day)
			self.eventlist.add_item(item,day,False)

		new_window.btn_complete.clicked.connect(create_new)

		layout = QVBoxLayout()
		action_bar = QHBoxLayout()


		self.title = QLabel(format_date(day) if separate else word("today"))

		if separate:
			self.resize(700,500)

		self.title.setStyleSheet(TITLE_STYLE)
		btn_new = QPushButton("+")
		btn_new.setMaximumSize(50,50)
		btn_new.setStyleSheet(ADD_BUTTON_STYLE)
		btn_new.clicked.connect(show_new)
		action_bar.addWidget(self.title)
		action_bar.addWidget(btn_new)
		layout.addLayout(action_bar)
		layout.addWidget(self.eventlist)
		self.setLayout(layout)

	def set_light(self):
		self.title.setStyleSheet()
	def set_dark(self):...
