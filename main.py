import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap,QImage
from main_window import MainWindow
import model
from multiprocessing import Process
from threading import Thread, Event

if __name__ == "__main__":
	app = QApplication()
	img:QPixmap = QPixmap()
	img.load("icon.png")
	app.setWindowIcon(img)
	win = MainWindow()
	#win.setWindowTitle("LiveSmarter")
	win.resize(900,600)

	win.show()

	print("Starting")

	signal = Event()

	#signal.set()

	listener = Thread(target=model.notificationListener,args=[signal])

	listener.start()

	app.exec()

	signal.set()

