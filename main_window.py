from copy import deepcopy
from functools import partial
from typing import override
from datetime import date as ddate
from PySide6.QtWidgets import QApplication,QMenu,QMainWindow,QListWidget,QComboBox,QMessageBox,QFrame,QSpacerItem,QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QSizePolicy,QLabel,QTabWidget
from PySide6.QtGui import QPixmap
import model
from data import *
from editor import NewEventWindow
from model import get_active_dates, load_all, Event, save_item
from task_list import EventList, ActiveDatesList,DayPreview


def menu_button_size(widgets:list[QWidget]):
	for element in widgets:
		element.setFixedHeight(38)

class Sidebar(QFrame):
	@override
	def __init__(self):
		super().__init__()
		main_layout = QVBoxLayout()
		layout = QVBoxLayout()

		pm_today = QPixmap()
		pm_today.load("icons/home.png")

		pm_calendar = QPixmap()
		pm_calendar.load("icons/calendar.png")

		pm_timetables = QPixmap()
		pm_timetables.load("icons/timetables.png")

		self.btn_today = QPushButton(" сегодня")
		self.btn_today.setIcon(pm_today)

		self.btn_calendar = QPushButton(" календарь")
		self.btn_calendar.setIcon(pm_calendar)

		self.btn_timetables = QPushButton(" расписания")
		self.btn_timetables.setIcon(pm_timetables)

		self.setFixedWidth(200)

		self.btn_today.setStyleSheet(SIDEBAR_BUTTON_STYLE_SELECTED)
		self.btn_calendar.setStyleSheet(SIDEBAR_BUTTON_STYLE)
		self.btn_timetables.setStyleSheet(SIDEBAR_BUTTON_STYLE)
		menu_button_size([self.btn_today,self.btn_calendar])
		layout.addWidget(self.btn_today)
		layout.addWidget(self.btn_calendar)
		layout.addWidget(self.btn_timetables)
		main_layout.addLayout(layout)
		self.setLayout(main_layout)

		self.setStyleSheet("""
        background-color:#3B9AFF;
        padding:12;
        border-radius:10;
        """)








class CalendarWindow(QWidget):
	@override
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()
		self.selected_year:int = ddate.today().year
		self.selected_month:int = ddate.today().month
		title_layout = QHBoxLayout()
		self.title = QLabel(f"{MONTHS["RUSSIAN"][self.selected_month-1]} {self.selected_year} г.")
		buttons = QHBoxLayout()
		btn_next = QPushButton(">")
		btn_back = QPushButton("<")
		btn_new = QPushButton("+")
		btn_new.setStyleSheet(ADD_BUTTON_STYLE)
		btn_new.setMaximumSize(50,50)
		select_sort_mode = QComboBox()
		select_sort_mode.addItems(["дате","количеству задач"])

		win_create = NewEventWindow()

		title_layout.addWidget(self.title)
		#title_layout.addSpacerItem(QSpacerItem(100,0))
		title_layout.addWidget(btn_new)

		def open_new():
			win_create.show()

		def create_new():
			win_create.create_new()
			update_dates()

		def update_title():
			self.title.setText(f"{MONTHS["RUSSIAN"][self.selected_month-1]} {self.selected_year} г.")

		def next_month():
			if self.selected_month < 12:
				self.selected_month+=1
			else:
				self.selected_month = 1
				self.selected_year+=1
			update_title()
			update_dates()
		def back():
			if self.selected_month > 1:
				self.selected_month -= 1
			else:
				self.selected_month = 12
				self.selected_year -= 1
			update_title()
			update_dates()


		buttons.addWidget(btn_back)
		buttons.addWidget(btn_next)
		buttons.addWidget(QLabel("Сортировать по"))
		buttons.addWidget(select_sort_mode)



		btn_next.clicked.connect(next_month)
		win_create.btn_complete.clicked.connect(create_new)
		btn_back.clicked.connect(back)
		btn_new.clicked.connect(open_new)
		buttons.addSpacerItem(QSpacerItem(100,0))
		self.title.setStyleSheet(TITLE_STYLE)
		data = get_active_dates(self.selected_year, self.selected_month)
		self.list_dates = ActiveDatesList([(i,WEEKDAYS["RUSSIAN"][(d:=ddate(self.selected_year,self.selected_month,int(i))).weekday()],str(data[i]),d) for i in data])
		def update_dates():
			data2 = get_active_dates(self.selected_year,self.selected_month)
			print(self.selected_year,self.selected_month)
			self.list_dates.reset_data([(i,WEEKDAYS["RUSSIAN"][(d:=ddate(self.selected_year,self.selected_month,int(i))).weekday()],str(data2[i]),d) for i in data2])
		layout.addLayout(title_layout)
		layout.addWidget(self.list_dates)
		layout.addLayout(buttons)

		self.setLayout(layout)

class TimetablesWindow(QWidget):
	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()

		self.selected_weekday = 1

		self.title = QLabel()

		self.title.setStyleSheet(TITLE_STYLE)

		btn_new = QPushButton("+")
		btn_new.setStyleSheet(ADD_BUTTON_STYLE)
		btn_new.setFixedSize(50,50)
		title_layout = QHBoxLayout()
		title_layout.addWidget(self.title)
		title_layout.addWidget(btn_new)

		buttons = QHBoxLayout()
		btn_next = QPushButton(">")
		btn_back = QPushButton("<")
		buttons.addWidget(btn_back)
		buttons.addWidget(btn_next)
		buttons.addSpacerItem(QSpacerItem(200, 0))

		self.event_list = EventList(model.get_timetable(self.selected_weekday),self.selected_weekday)

		def update():
			self.title.setText(WEEKDAYS["RUSSIAN"][self.selected_weekday-1])
			self.event_list.reset_data(model.get_timetable(self.selected_weekday),self.selected_weekday,isTimetable=True)

		update()

		def next_weekday():
			if self.selected_weekday < 7:
				self.selected_weekday+=1
			else:
				self.selected_weekday = 1
			update()

		def previous_weekday():
			if self.selected_weekday > 1:
				self.selected_weekday -= 1
			else:
				self.selected_weekday = 7
			update()

		btn_next.clicked.connect(next_weekday)
		btn_back.clicked.connect(previous_weekday)
		layout.addLayout(title_layout)
		layout.addWidget(self.event_list)
		layout.addLayout(buttons)
		self.setLayout(layout)

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		layout = QHBoxLayout()
		sidebar = Sidebar()
		layout.addWidget(sidebar)
		today_window = DayPreview(ddate.today())
		layout.addWidget(today_window)


		TABS:dict[str,QWidget] = {
			"today":today_window,
			"calendar":CalendarWindow(),
			"timetables":TimetablesWindow(),
		}


		def set_tab(tab:str):
			layout.itemAt(1).widget().setParent(None)
			layout.addWidget(TABS[tab])

		def set_today():
			set_tab("today")
			sidebar.btn_today.setStyleSheet(SIDEBAR_BUTTON_STYLE_SELECTED)
			sidebar.btn_calendar.setStyleSheet(SIDEBAR_BUTTON_STYLE)
			sidebar.btn_timetables.setStyleSheet(SIDEBAR_BUTTON_STYLE)


		def set_calendar():
			set_tab("calendar")
			sidebar.btn_calendar.setStyleSheet(SIDEBAR_BUTTON_STYLE_SELECTED)
			sidebar.btn_today.setStyleSheet(SIDEBAR_BUTTON_STYLE)
			sidebar.btn_timetables.setStyleSheet(SIDEBAR_BUTTON_STYLE)


		def set_timetables():
			set_tab("timetables")
			sidebar.btn_calendar.setStyleSheet(SIDEBAR_BUTTON_STYLE)
			sidebar.btn_today.setStyleSheet(SIDEBAR_BUTTON_STYLE)
			sidebar.btn_timetables.setStyleSheet(SIDEBAR_BUTTON_STYLE_SELECTED)

		sidebar.btn_today.clicked.connect(set_today)
		sidebar.btn_calendar.clicked.connect(set_calendar)
		sidebar.btn_timetables.clicked.connect(set_timetables)
		self.setLayout(layout)
		#self.menuBar().addMenu(QMenu("Hello"))





