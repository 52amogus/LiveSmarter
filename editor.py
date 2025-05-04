from datetime import datetime

from data import TITLE_STYLE, SUBTITLE_STYLE, ADD_BUTTON_STYLE, MAIN_BUTTON_STYLE
from model import Event,save_item
from PySide6.QtWidgets import QSizePolicy,QCheckBox,QComboBox,QInputDialog,QSpacerItem,QHBoxLayout,QVBoxLayout,QLabel,QWidget, QLineEdit, QPushButton, QDateTimeEdit, QFormLayout
from PySide6.QtCore import Qt
#from PySide6.QtGui import

class EditorRow(QWidget):
    def __init__(self,title,enter_widget:QWidget,horizontal=False):
        super().__init__()
        layout = QHBoxLayout() if horizontal else QVBoxLayout()
        title = QLabel(title)
        title.setStyleSheet(SUBTITLE_STYLE)
        enter_widget.setStyleSheet("""
        font-size:15px;
        font-weight:500px;
        """)
        self.enter = enter_widget
        layout.addWidget(title)
        self.enter.setFixedHeight(30)
        layout.addWidget(self.enter)
        if horizontal:
            layout.addSpacerItem(QSpacerItem(200,0))
        self.setLayout(layout)




class NewEventWindow(QWidget):
    def __init__(self,defaultDateTime=datetime.today()):
        super().__init__()
        self.name_enter = EditorRow("Имя",QLineEdit())
        self.date_time_edit = EditorRow("Дата и время",QDateTimeEdit())
        self.date_time_edit.enter.setDateTime(defaultDateTime)
        self.resize(500,300)
        self.btn_complete = QPushButton("Создать")
        self.choose_tags = EditorRow("Теги",QComboBox())
        self.choose_tags.enter.addItems(["Нет","Новый"])
        self.isImportant = EditorRow("Важное",QCheckBox(),horizontal=True)


        main_layout = QVBoxLayout()

        title = QLabel("Новая задача")
        title.setStyleSheet(TITLE_STYLE)

        self.btn_complete.setStyleSheet(MAIN_BUTTON_STYLE)
        self.btn_complete.setFixedSize(200,50)

        main_layout.addWidget(title,alignment=Qt.AlignmentFlag.AlignCenter)

        def select_tag():
            QInputDialog().getText(QLineEdit(),"2","3")
            self.choose_tags.enter.setItemText(self.choose_tags.enter.currentIndex(),"NEW!!")
        self.choose_tags.enter.currentIndexChanged.connect(select_tag)


        for widget in [self.name_enter,self.date_time_edit,self.choose_tags,self.isImportant]:
            main_layout.addWidget(widget)

        main_layout.addWidget(self.btn_complete,alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def create_new(self) -> Event:
        item = Event(self.name_enter.enter.text(), self.date_time_edit.enter.time().toPython(),self.isImportant.enter.isChecked())
        save_item(self.date_time_edit.enter.date().toPython(), item)
        self.close()
        return item



    def get_result(self):
        return (self.date_time_edit.dateTime().toPyDateTime(),
                {"name":self.name_enter.text(),
                 "time":self.date_time_edit.time().toPyTime().isoformat(),
                 "version": "1.0"})