from datetime import datetime,date
from data import TITLE_STYLE, SUBTITLE_STYLE, ADD_BUTTON_STYLE, MAIN_BUTTON_STYLE
from model import Event,save_item,save_to_timetable
from PySide6.QtWidgets import QSizePolicy,QTimeEdit,QCheckBox,QComboBox,QInputDialog,QSpacerItem,QHBoxLayout,QVBoxLayout,QLabel,QWidget, QLineEdit, QPushButton, QDateTimeEdit, QFormLayout
from PySide6.QtCore import QTime,Qt
from localization import word

class NewEventWindow(QWidget):
	def __init__(self,
				 requires_full_datetime:bool = False,
				 default_year=None,
				 default_month=None):
		super().__init__()

		self.requires_date = requires_full_datetime

		self.name_enter = QLineEdit()

		if requires_full_datetime:
			self.date_time_edit = QDateTimeEdit()
			self.date_time_edit.setDateTime(datetime(year=default_year,
													 month=default_month,
													 day=1))
		else:
			self.date_time_edit = QTimeEdit()
			self.date_time_edit.setTime(datetime.now().time())

		self.setFixedSize(320,240)
		self.btn_complete = QPushButton(word("create"))
		self.choose_tags = QComboBox()
		self.choose_tags.addItems([word("no_tags"),word("new_tag")])
		self.isImportant = QCheckBox()


		main_layout = QFormLayout()

		title = QLabel(word("new_event"))
		title.setStyleSheet("""
		font-size:25px;
		font-weight:900;
		""")

		self.btn_complete.setStyleSheet(MAIN_BUTTON_STYLE)
		self.btn_complete.setFixedSize(100,40)

		main_layout.setFormAlignment(Qt.AlignmentFlag.AlignVCenter)

		main_layout.addRow(title)

		main_layout.addRow(word("event_name"),self.name_enter)
		main_layout.addRow(word("event_datetime"),self.date_time_edit)
		main_layout.addRow(word("event_is_important"),self.isImportant)
		main_layout.addRow(word("event_tags"),self.choose_tags)

		main_layout.addRow(self.btn_complete)

		self.setLayout(main_layout)

	def create_new(self,save_date:date=None,isTimetable:bool=False,weekday:int=None) -> Event|tuple[object,Event]:
		text = self.name_enter.text()
		if text == "":
			text = "Без названия"
		item = Event(text, self.date_time_edit.time().toPython(),self.isImportant.isChecked())
		print("TI",item.id)
		if isTimetable:
			save_to_timetable(weekday,item)
		else:
			if save_date is None:
				save_date = self.date_time_edit.date().toPython()
			save_item(
				save_date,
				item)


		self.close()
		if self.requires_date:
			return self.date_time_edit.date().toPython(),item
		return item


	def get_result(self):
		return (self.date_time_edit.dateTime().toPyDateTime(),
				{"name":self.name_enter.text(),
				 "time":self.date_time_edit.time().toPyTime().isoformat(),
				 "version": "1.0"})

	def setDefault(self,year,month):
		self.date_time_edit.setDateTime(datetime(year=year,month=month,day=1))