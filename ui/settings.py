from PySide6.QtWidgets import QApplication,QWidget,QMessageBox,QHBoxLayout,QLabel,QPushButton,QVBoxLayout,QCheckBox,QComboBox
from localization import word
import model
from data import *
from model import get_setting,set_setting

LANGUAGES = {
	"ru_RU":"Русский",
	"en_US":"English"
}

class SettingsWindow(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()

		title = QLabel(word("settings"))
		title.setStyleSheet(SUBTITLE_STYLE)

		restart_notice = QMessageBox()
		restart_notice.setText("Изменение применится только после перезапуска приложения")

		def set_language(new_index):
			model.set_setting("language",list(LANGUAGES.keys())[new_index])
			restart_notice.show()

		select_language = QComboBox()
		languages = list(LANGUAGES.values())
		select_language.addItems(languages)
		current_language = model.get_setting("language")
		select_language.setCurrentIndex(list(LANGUAGES.keys()).index(current_language))

		btn_new = QPushButton(word("custom_lang"))
		btn_search = QPushButton(word("load_lang"))

		select_ln_layout = QHBoxLayout()
		select_ln_layout.addWidget(select_language)
		select_ln_layout.addWidget(btn_new)
		select_ln_layout.addWidget(btn_search)


		layout.addWidget(title)
		layout.addWidget(QLabel(word("lang")))
		layout.addLayout(select_ln_layout)

		select_language.currentIndexChanged.connect(set_language)

		self.setLayout(layout)

