from PySide6.QtWidgets import QApplication,QSystemTrayIcon,QLabel
from PySide6.QtGui import QPixmap
from ui.main_windows import MainWindow
import model,platform
from threading import Thread, Event


if __name__ == "__main__":
	app = QApplication([])
	img = QPixmap()
	img.load("icons/icon.png")
	app.setWindowIcon(img)
	win = MainWindow(app.styleHints().colorScheme())
	win.setWindowTitle("Reminders")
	win.resize(900,600)

	os = platform.platform()

	win.show()

	print("Starting")

	signal = Event()


	tray = QSystemTrayIcon()
	tray.setVisible(True)
	tray.setIcon(img)



	"""if platform.platform()[:5] == "macOS":
		listener = Thread(target=model.notificationListener,args=[signal])


		listener.start()"""

	app.exec()

	signal.set()

