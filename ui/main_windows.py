from typing import override
from datetime import date as ddate
from PySide6.QtWidgets import QApplication,QMenu,QMenuBar,QMainWindow,QListWidget,QComboBox,QMessageBox,QFrame,QSpacerItem,QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QSizePolicy,QLabel,QTabWidget
from PySide6.QtGui import QPixmap,QAction
from PySide6.QtCore import QEvent,Qt,Signal
import model
from data import *
from .new_event import NewEventWindow
from model import get_active_dates, load_all, Event, save_item
from .eventlist import EventList
from .datelist import ActiveDatesList
from .day_preview import DayPreview
from localization import word
from .settings import SettingsWindow
import webbrowser

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

		self.btn_today = QPushButton(f" {word("today")}")
		self.btn_today.setIcon(pm_today)

		self.btn_calendar = QPushButton(f" {word("calendar")}")
		self.btn_calendar.setIcon(pm_calendar)

		self.btn_timetables = QPushButton(f" {word("timetables")}")
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

	def set_dark_mode(self):
		self.setStyleSheet("""
        background-color:#404040;
        padding:12;
        border-radius:10;
        """)
	def set_light_mode(self):
		self.setStyleSheet("""
		background-color:#CCCCCC;
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
		self.title = QLabel(f"{word("months")[self.selected_month-1]} {self.selected_year}")
		buttons = QHBoxLayout()
		btn_next = QPushButton(">")
		btn_back = QPushButton("<")
		btn_new = QPushButton("+")
		btn_new.setStyleSheet(ADD_BUTTON_STYLE)
		btn_new.setMaximumSize(50,50)
		select_sort_mode = QComboBox()
		select_sort_mode.addItems(["дате","количеству задач"])

		self.win_create = NewEventWindow(
			requires_full_datetime=True,
			default_year=self.selected_year,
			default_month=self.selected_month
		)

		title_layout.addWidget(self.title)
		event = QEvent(QEvent.Type.ThemeChange)
		title_layout.addWidget(btn_new)

		def update_title():
			self.title.setText(f"{word("months")[self.selected_month-1]} {self.selected_year}")

		def next_month():
			if self.selected_month < 12:
				self.selected_month+=1
			else:
				self.selected_month = 1
				self.selected_year+=1
			update_title()
			self.update_dates()
			self.win_create.setDefault(self.selected_year,self.selected_month)
		def back():
			if self.selected_month > 1:
				self.selected_month -= 1
			else:
				self.selected_month = 12
				self.selected_year -= 1
			update_title()
			self.update_dates()
			self.win_create.setDefault(self.selected_year, self.selected_month)


		buttons.addWidget(btn_back)
		buttons.addWidget(btn_next)
		#buttons.addWidget(QLabel("Сортировать по"))
		#buttons.addWidget(select_sort_mode)
		btn_next.clicked.connect(next_month)
		self.win_create.btn_complete.clicked.connect(self.create_new)
		btn_back.clicked.connect(back)
		btn_new.clicked.connect(self.open_new)
		buttons.addSpacerItem(QSpacerItem(200,0))
		self.title.setStyleSheet(TITLE_STYLE)
		data = get_active_dates(self.selected_year, self.selected_month)
		self.list_dates = ActiveDatesList([date(self.selected_year,self.selected_month,int(i)) for i in get_active_dates(self.selected_year,self.selected_month)])
		layout.addLayout(title_layout)
		layout.addWidget(self.list_dates)
		layout.addLayout(buttons)

		self.setLayout(layout)

	def update(self):
		data2 = get_active_dates(self.selected_year, self.selected_month)
		print(self.selected_year, self.selected_month)
		self.list_dates.reset_data([(i, word("weekdays")[
			(d := ddate(self.selected_year, self.selected_month, int(i))).weekday()], str(data2[i]), d) for i in data2])

	def open_new(self):
		self.win_create.show()

	def create_new(self):
		self.win_create.create_new()
		self.update()

class AboutWindow(QWidget):
	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()

		icon = QPixmap()
		icon.load("icons/icon_small.png")

		lb_icon = QLabel()
		lb_icon.setPixmap(icon)

		def open_github():
			webbrowser.open("https://github.com/52amogus/LiveSmarter")

		title = QLabel("О приложении")
		title.setStyleSheet(SUBTITLE_STYLE)

		contribute = QPushButton("GitHub")
		contribute.clicked.connect(open_github)

		layout.addWidget(lb_icon)
		layout.addWidget(title)
		layout.addWidget(contribute)

		self.setFixedSize(230,300)


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
			self.title.setText(word("weekdays")[self.selected_weekday-1])
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

class MainWindow(QMainWindow):
	def __init__(self,initialTheme):
		super().__init__()
		layout = QHBoxLayout()
		self.sidebar = Sidebar()
		layout.addWidget(self.sidebar)
		today_window = DayPreview(ddate.today())
		layout.addWidget(today_window)
		TABS: dict[str, QWidget] = {
			"today": today_window,
			"calendar": CalendarWindow(),
			"timetables": TimetablesWindow(),
		}

		mb = self.menuBar()
		main_menu = QMenu(word("mb_event"))
		new_action = QAction(word("mb_new"), self)
		settings_action = QAction("settings",self)
		about_action = QAction("about",self)

		new_action.triggered.connect(TABS["calendar"].open_new)
		settings_action.triggered.connect(self.open_settings)
		about_action.triggered.connect(self.about)

		main_menu.addAction(new_action)
		main_menu.addAction(settings_action)
		main_menu.addAction(about_action)
		mb.addMenu(main_menu)

		widget = QWidget()




		def set_tab(tab:str):
			layout.itemAt(1).widget().setParent(None)
			layout.addWidget(TABS[tab])

		def set_today():
			set_tab("today")
			self.sidebar.btn_today.setStyleSheet(SIDEBAR_BUTTON_STYLE_SELECTED)
			self.sidebar.btn_calendar.setStyleSheet(SIDEBAR_BUTTON_STYLE)
			self.sidebar.btn_timetables.setStyleSheet(SIDEBAR_BUTTON_STYLE)


		def set_calendar():
			set_tab("calendar")
			self.sidebar.btn_calendar.setStyleSheet(SIDEBAR_BUTTON_STYLE_SELECTED)
			self.sidebar.btn_today.setStyleSheet(SIDEBAR_BUTTON_STYLE)
			self.sidebar.btn_timetables.setStyleSheet(SIDEBAR_BUTTON_STYLE)


		def set_timetables():
			set_tab("timetables")
			self.sidebar.btn_calendar.setStyleSheet(SIDEBAR_BUTTON_STYLE)
			self.sidebar.btn_today.setStyleSheet(SIDEBAR_BUTTON_STYLE)
			self.sidebar.btn_timetables.setStyleSheet(SIDEBAR_BUTTON_STYLE_SELECTED)

		self.sidebar.btn_today.clicked.connect(set_today)
		self.sidebar.btn_calendar.clicked.connect(set_calendar)
		self.sidebar.btn_timetables.clicked.connect(set_timetables)
		self.settings_window = SettingsWindow()
		self.about_window = AboutWindow()
		widget.setLayout(layout)
		self.theme = initialTheme
		self.setCentralWidget(widget)

		if self.theme == Qt.ColorScheme.Dark:
			self.sidebar.set_dark_mode()
			self.theme = Qt.ColorScheme.Dark
		else:
			self.sidebar.set_light_mode()
			self.theme = Qt.ColorScheme.Light


	def changeEvent(self, event:QEvent):
		if event.type() == QEvent.Type.ThemeChange:
			if self.theme == Qt.ColorScheme.Light:
				self.sidebar.set_dark_mode()
				self.theme = Qt.ColorScheme.Dark
			else:
				self.sidebar.set_light_mode()
				self.theme = Qt.ColorScheme.Light
		event.accept()
		super().changeEvent(event)

	def about(self):
		self.about_window.show()

	def open_settings(self):
		self.settings_window.show()




