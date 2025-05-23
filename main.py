from PySide6.QtWidgets import QApplication,QMenu,QMenuBar,QSystemTrayIcon,QLabel
from PySide6.QtGui import QPixmap,QImage,QAction,QActionGroup
from PySide6.QtCore import Qt,QPoint
from ui.main_windows import MainWindow
import model,platform
from threading import Thread, Event

if __name__ == "__main__":
	app = QApplication([])
	img = QPixmap()
	img.load("icons/icon.png")
	app.setWindowIcon(img)
	win = MainWindow(app.styleHints().colorScheme())
	win.setWindowTitle("LiveSmarter")
	win.resize(900,600)

	os = platform.platform()

	win.show()

	print("Starting")

	signal = Event()


	tray = QSystemTrayIcon()
	tray.setVisible(True)
	tray.setIcon(img)


	#win.setAttribute(Qt.ApplicationAttribute.AA_UseOpenGLES, True)
	app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, False)

	if platform.platform()[:5] == "macOS":
		listener = Thread(target=model.notificationListener,args=[signal])


		listener.start()

	app.exec()

	signal.set()

