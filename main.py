from PySide6.QtWidgets import QApplication,QMenu,QSystemTrayIcon,QLabel
from sys import argv
from PySide6.QtGui import QPixmap,QImage,QAction,QActionGroup
from ui.main_windows import MainWindow
import model
from threading import Thread, Event

if __name__ == "__main__":
	app = QApplication(argv)
	img = QPixmap()
	img.load("icon.png")
	app.setWindowIcon(img)
	win = MainWindow(app.styleHints().colorScheme())
	win.setWindowTitle("LiveSmarter")
	win.resize(900,600)

	win.show()

	print("Starting")

	signal = Event()


	tray = QSystemTrayIcon()
	tray.setVisible(True)
	tray.setIcon(img)



	listener = Thread(target=model.notificationListener,args=[signal])

	listener.start()

	app.exec()

	signal.set()

