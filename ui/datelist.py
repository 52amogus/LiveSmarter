from PySide6.QtWidgets import QFrame,QLabel,QAbstractItemView,QVBoxLayout,QHBoxLayout,QPushButton,QListWidget,QListWidgetItem
from PySide6.QtCore import Qt
from .day_preview import DayPreview
from data import *
from localization import word
from datetime import date
import model

class EmptyDateRow(QFrame):
	def __init__(self,items_date):
		super().__init__()
		layout = QHBoxLayout()
		self.date = items_date

		name = QLabel(QLabel(f"{word("weekdays")[self.date.weekday()]}, "
						 f"{format_component(items_date.day)}.{format_component(items_date.month)}"))

		layout.addWidget(name)
		self.setStyleSheet(UNDEFINED_ROW_STYLE)
		self.setLayout(layout)

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton:
			self.show_preview()

	def show_preview(self):
		DayPreview(self.date, separate=True).show()


class ActiveDateRow(QFrame):
	def __init__(self, items_date:date):
		super().__init__()
		self.setStyleSheet(LIST_ROW_STYLE)
		self.date = items_date

		main_layout = QVBoxLayout()

		all_items = model.load_all(items_date)
		important_items_names = [i.name for i in all_items if i.isImportant]
		layout = QHBoxLayout()
		tx_date = QLabel(f"{word("weekdays")[self.date.weekday()]}, "
						 f"{format_component(items_date.day)}.{format_component(items_date.month)}")
		tx_amount = QLabel(str(len(all_items)))
		tx_amount.setStyleSheet("""
                    border-radius:20;
                    background-color:white;
                    color:#3B9AFF;
                    padding:10;
                    """)

		important_items_layout = QHBoxLayout()
		important_items = [QLabel(item) for item in important_items_names]
		for widget in important_items:
			widget.setStyleSheet(LIST_LAYER2_STYLE)
			important_items_layout.addWidget(widget)


		tx_amount.setMaximumSize(40,40)
		layout.addWidget(tx_date)
		layout.addWidget(tx_amount)

		main_layout.addLayout(layout)
		main_layout.addLayout(important_items_layout)

		self.setLayout(main_layout)

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton:
			self.show_preview()

	def show_preview(self):
		DayPreview(self.date, separate=True).show()


class ActiveDatesList(QListWidget):
	def __init__(self,all_items:list[date]):
		super().__init__()
		self.setObjectName("activeDatesList")
		self.setSpacing(20)
		for item in all_items:
			self.add_item(item)
		self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

	def reset_data(self,new:list[date]):
		self.clear()
		for item in new:
			self.add_item(item)

	def add_item(self,item:date):
		list_item = QListWidgetItem(self)
		widget_item = ActiveDateRow(item)
		self.addItem(list_item)
		list_item.setSizeHint(widget_item.sizeHint())
		self.setItemWidget(list_item, widget_item)