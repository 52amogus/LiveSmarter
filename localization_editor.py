"""
An application for adding new languages to LiveSmarter
"""
import sys
from PySide6.QtWidgets import QApplication,QTextEdit,QInputDialog,QFileDialog,QFormLayout,QLineEdit,QComboBox,QPushButton,QVBoxLayout,QHBoxLayout,QListWidget,QWidget
import json

app = QApplication()


win = QWidget()

language_name = QInputDialog.getText(QLineEdit(),"create a localization","name in the language you are adding")

if language_name[0] == "":
	sys.exit()

words_list = QListWidget()

buttons = QHBoxLayout()

btn_new = QPushButton("+")
btn_edit = QPushButton("edit")
btn_delete = QPushButton("delete")
btn_save = QPushButton("save")

win.resize(400,300)

buttons.addWidget(btn_new)
buttons.addWidget(btn_edit)
buttons.addWidget(btn_delete)
buttons.addWidget(btn_save)


keywords = [
	"today",
	"calendar",
	"timetables",
	"new_event",
	"event_name",
	"event_datetime",
	"event_is_important",
	"event_tags",
	"new_tag",
	"no_tags",
	"create",
	"months",
	"months2",
	"weekdays"
]

result = {}


new_keyword_window = QWidget()
new_keyword_window.setWindowTitle("New localization")
pick_keyword = QComboBox()
pick_keyword.addItems(keywords)
btn_add = QPushButton("Add")
enter_value = QLineEdit()
enter_values = QTextEdit()

layout = QFormLayout()
layout.addRow("keyword",pick_keyword)
layout.addRow("localization",enter_value)
layout.addWidget(btn_add)
new_keyword_window.setLayout(layout)

requires_list = [
	"months",
	"months2",
	"weekdays"
]

result["localization_name"] = language_name[0]

def add_localization_start():
	new_keyword_window.show()

def set_enter_date_type(new):
	if new in requires_list:
		layout.replaceWidget(enter_value,enter_values)
	else:
		layout.replaceWidget(enter_values, enter_value)

def add_localization():
	result[pick_keyword.currentText()] = enter_value.text()
	new_keyword_window.close()
	words_list.addItem(f"{pick_keyword.currentText()} - {enter_value.text()}")

def save_localization():
	filename = QFileDialog().getSaveFileName()
	if filename[0] != "":
		with open(f"{filename[0]}.json","w",encoding="us-ascii") as file:
			json.dump(result,file)
		app.quit()

main_layout = QVBoxLayout()
main_layout.addWidget(words_list)
main_layout.addLayout(buttons)


btn_new.clicked.connect(add_localization_start)
btn_add.clicked.connect(add_localization)
btn_save.clicked.connect(save_localization)
pick_keyword.currentTextChanged.connect(set_enter_date_type)

win.setLayout(main_layout)
win.setWindowTitle("LiveSmarter localization editor")
win.show()
app.exec()

