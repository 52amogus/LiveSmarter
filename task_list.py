from typing import NamedTuple

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QListWidget,
                               QHeaderView,
                                QCheckBox,
                               QHBoxLayout,
                               QVBoxLayout,
                               QLabel,
                               QListWidgetItem,
                               QWidget,
                                QPushButton,
                               QFrame,
                               QAbstractItemView)
from PySide6.QtCore import Qt
from model import Event
from data import *
from datetime import timedelta, date as ddate, datetime
from model import load_all
from editor import NewEventWindow

LIST_ROW_STYLE = """
background-color:#3B9AFF;
border-radius:10;
font-size:20px;
font-weight:600;
color:white;
"""

IMPORTANT_ROW_STYLE = """
background-color:#FF4C4C;
border-radius:10;
font-size:20px;
font-weight:900;
color:white;
"""


class EventRow(QFrame):
    def __init__(self,item:Event):
        super().__init__()
        print(item.name)
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

        isChecked = QCheckBox()
        isChecked.setFixedSize(50,50)

        main_lay.addWidget(isChecked)
        main_lay.addLayout(lay)

        self.setLayout(main_lay)
        self.setObjectName("eventFrame")
        self.setStyleSheet(IMPORTANT_ROW_STYLE if item.isImportant else LIST_ROW_STYLE)



class EventList(QListWidget):
    def __init__(self,all_items:list[Event]):
        super().__init__()
        self.setObjectName("eventList")
        self.setSpacing(20)
        for item in all_items:
            self.add_item(item)


    def reset_data(self,new:list[Event]):
        self.clear()
        for item in new:
            self.add_item(item)
    def add_item(self,item:Event):
        list_item = QListWidgetItem(self)
        widget_item = EventRow(item)
        self.addItem(list_item)
        list_item.setSizeHint(widget_item.sizeHint())
        self.setItemWidget(list_item, widget_item)

class DayPreview(QWidget):
    def __init__(self,day:ddate,separate=False):
        super().__init__()
        new_window = NewEventWindow(defaultDateTime=datetime(day.year,day.month,day.day) if separate else datetime.today())

        date = day
        self.eventlist = EventList(load_all(date))

        def show_new():
            new_window.show()

        def create_new():
            item = new_window.create_new()
            self.eventlist.add_item(item)

        new_window.btn_complete.clicked.connect(create_new)

        layout = QVBoxLayout()
        action_bar = QHBoxLayout()

        title = QLabel(format_date(day) if separate else "Сегодня")

        if separate:
            self.resize(700,500)

        title.setStyleSheet(TITLE_STYLE)
        btn_new = QPushButton("+")
        btn_new.setMaximumSize(50,50)
        btn_new.setStyleSheet(ADD_BUTTON_STYLE)
        btn_new.clicked.connect(show_new)
        action_bar.addWidget(title)
        action_bar.addWidget(btn_new)
        layout.addLayout(action_bar)
        layout.addWidget(self.eventlist)
        self.setLayout(layout)

class ActiveDateRow(QFrame):
    def __init__(self, day:tuple[str,str,str,ddate]):
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
    def __init__(self,all_items:list[tuple[str,str,str,ddate]]):
        super().__init__()
        self.setObjectName("activeDatesList")
        self.setSpacing(20)
        for item in all_items:
            self.add_item(item)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def reset_data(self,new:list[tuple[str,str,str,ddate]]):
        self.clear()
        for item in new:
            self.add_item(item)

    def add_item(self,item:tuple[str,str,str,ddate]):
        list_item = QListWidgetItem(self)
        widget_item = ActiveDateRow(item)
        self.addItem(list_item)
        list_item.setSizeHint(widget_item.sizeHint())
        self.setItemWidget(list_item, widget_item)