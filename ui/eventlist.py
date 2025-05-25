from PySide6.QtWidgets import QFrame,QHBoxLayout,QListWidgetItem,QVBoxLayout,QLabel,QCheckBox,QListWidget
from model import Event,save_to_timetable,save_item
from datetime import date as ddate
from data import *


class EventRow(QFrame):
	def __init__(self,item:Event,item_date:ddate|int,isTimetable):
		super().__init__()

		self.date = item_date

		main_lay = QHBoxLayout()
		lay = QVBoxLayout()
		lay.setSpacing(0)

		name_label = QLabel(item.name)
		lay.addWidget(name_label)

		time_label = QLabel(
			f"{item.time.hour} : {item.time.minute if item.time.minute > 9 else f"0{item.time.minute}"}"
		)
		name_label.setObjectName("subtitle")
		time_label.setObjectName("subtitle")

		lay.addWidget(time_label)

		self.isCompleted = QCheckBox()
		self.isCompleted.setChecked(item.completed)
		self.isCompleted.setFixedSize(50,50)

		def edit_completed():
			item.completed = True
			if isTimetable:
				save_to_timetable(item_date,item)
			else:
				save_item(self.date,item)


		self.isCompleted.checkStateChanged.connect(edit_completed)

		main_lay.addWidget(self.isCompleted)
		main_lay.addLayout(lay)

		self.setLayout(main_lay)
		self.setObjectName("eventFrame")
		self.setStyleSheet(IMPORTANT_ROW_STYLE if item.isImportant else LIST_ROW_STYLE)



class EventList(QListWidget):
	def __init__(self,all_items:list[Event],items_date:ddate|int,isTimetable=False):
		super().__init__()
		self.setObjectName("eventList")
		self.setSpacing(20)
		for item in all_items:
			self.add_item(item,items_date,isTimetable)


	def reset_data(self,new:list[Event],items_date:ddate,isTimetable):
		self.clear()
		for item in new:
			self.add_item(item,items_date,isTimetable)
	def add_item(self,item:Event,item_date:ddate|int,isTimetable):
		list_item = QListWidgetItem(self)
		widget_item = EventRow(item,item_date,isTimetable)
		self.addItem(list_item)
		list_item.setSizeHint(widget_item.sizeHint())
		self.setItemWidget(list_item, widget_item)