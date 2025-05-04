from data import MONTHS, WEEKDAYS
from editor import NewEventWindow
from model import Event
from task_list import EventList
from datetime import date,time

if __name__ == "__main__":
    from datetime import timedelta
    from mac_notifications import client
    from PySide6 import Qt
    import model
    from sys import argv
    from PySide6.QtWidgets import QLabel, QWidget, QApplication, QPushButton, QVBoxLayout, QListWidget, QHBoxLayout,QTabBar
    app = QApplication(argv)

    with open("stylesheet") as file:
        app.setStyleSheet(file.read())


    #Creating widgets
    main_layout = QHBoxLayout()

    list_days = QListWidget()

    selected_month = date.today().month
    selected_year = date.today().year

    list_days.addItems([f"{i},{WEEKDAYS["RUSSIAN"][date(selected_year, selected_month, int(i)).weekday()]}" for i in model.get_active_dates(selected_year, selected_month)])



    side_layout = QVBoxLayout()

    buttons = QHBoxLayout()

    btn_add = QPushButton("+")


    btn_next = QPushButton(">")
    btn_back = QPushButton("<")

    text_day = QLabel(f"{MONTHS["RUSSIAN"][selected_month-1]} {selected_year}г.")
    text_day.setObjectName("title")

    buttons.addWidget(btn_back)
    buttons.addWidget(btn_add)
    buttons.addWidget(btn_next)

    event_list = EventList([],date.today())

    #Adding widgets to the sidebar
    side_layout.addWidget(text_day)
    side_layout.addWidget(list_days)
    side_layout.addLayout(buttons)

    #Adding widgets to the main_layout
    main_layout.addLayout(side_layout)
    main_layout.addWidget(event_list)


    win = QWidget()

    win.setWindowTitle("LiveSmarter(desktop, PySide6)")


    win.setLayout(main_layout)

    win_add = NewEventWindow()

    win.resize(1000,800)

    def update_dates(year,month):
        list_days.clear()
        list_days.addItems([ f"{i},{WEEKDAYS[date(year,month,int(i)).weekday()]}" for i in model.get_active_dates(year, month)])
        win_add.close()

    #functions
    def new_event_start():
        win_add.show()

    def new_event():
        event = win_add.get_result()
        model.save_item(event[0],model.Event.decode(event[1]))
        update_dates(selected_year,selected_month)

    def open_day():
        event_list.reset_data(
            model.load_all(selected_date:=date(selected_year,selected_month,int(list_days.currentItem().text().split(",")[0]))),selected_date
        )

    def next_day():
        global selected_month,selected_year
        if selected_month < 12:
            selected_month+=1
        else:
            selected_month = 1
            selected_year+=1
        text_day.setText(f"{MONTHS["RUSSIAN"][selected_month-1]} {selected_year}г.")
        update_dates(selected_year,selected_month)

    def back():
        global selected_month,selected_year
        if selected_month > 1:
            selected_month-=1
        else:
            selected_month = 12
            selected_year-=1
        text_day.setText(f"{MONTHS["RUSSIAN"][selected_month-1]} {selected_year}г.")
        update_dates(selected_year, selected_month)

    #Actions
    btn_add.clicked.connect(new_event_start)
    win_add.btn_complete.clicked.connect(new_event)
    list_days.itemSelectionChanged.connect(open_day)
    btn_next.clicked.connect(next_day)
    btn_back.clicked.connect(back)


    win.show()
    app.exec()

