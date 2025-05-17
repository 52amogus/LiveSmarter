from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

app = QApplication([])
engine = QQmlApplicationEngine()
engine.load('file.qml')
engine.quit.connect(app.quit)
app.exec()