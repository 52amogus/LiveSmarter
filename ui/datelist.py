from PySide6.QtWidgets import QFrame,QLabel,QAbstractItemView,QVBoxLayout,QHBoxLayout,QPushButton,QListWidget,QListWidgetItem
from .day_preview import DayPreview
from data import *
from datetime import date


class ActiveDateRow(QFrame):
	def __init__(self, day:tuple[str,str,str,date]):
		super().__init__()
		self.setStyleSheet(LIST_ROW_STYLE)
		self.date = day[3]
		layout = QHBoxLayout()
		tx_date = QLabel(f"{day[1]}, {format_component(day[3].day)}.{format_component(day[3].month)}")
		tx_amount = QLabel(day[2])
		tx_amount.setStyleSheet("""
                    border-radius:20;
                    background-color:white;
                    color:#3B9AFF;
                    padding:10;
                    """)

		def show_preview():
			DayPreview(self.date,separate=True).show()


		self.btn_go = QPushButton("Перейти")
		self.btn_go.setStyleSheet("""
        padding:10;
        border:2px solid white 10px;
        """)
		self.btn_go.setMaximumSize(120,50)
		self.btn_go.clicked.connect(show_preview)

		#layout.setSpacing(0)

		tx_amount.setMaximumSize(40,40)
		layout.addWidget(tx_date)
		layout.addWidget(tx_amount)
		layout.addWidget(self.btn_go)


		self.setLayout(layout)



class ActiveDatesList(QListWidget):
	def __init__(self,all_items:list[tuple[str,str,str,date]]):
		super().__init__()
		self.setObjectName("activeDatesList")
		self.setSpacing(20)
		for item in all_items:
			self.add_item(item)
		self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

	def reset_data(self,new:list[tuple[str,str,str,date]]):
		self.clear()
		for item in new:
			self.add_item(item)

	def add_item(self,item:tuple[str,str,str,date]):
		list_item = QListWidgetItem(self)
		widget_item = ActiveDateRow(item)
		self.addItem(list_item)
		list_item.setSizeHint(widget_item.sizeHint())
		self.setItemWidget(list_item, widget_item)