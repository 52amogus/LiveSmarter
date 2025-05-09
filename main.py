from PySide6.QtWidgets import QApplication,QMessageBox,QLabel
from PySide6.QtGui import QPixmap,QImage
from main_window import MainWindow
from model import Event

if __name__ == "__main__":
    help(Event)
    app = QApplication()
    img:QPixmap = QPixmap()
    img.load("icon.png")
    app.setWindowIcon(img)
    win = MainWindow()
    win.setWindowTitle("LiveSmarter")
    win.resize(900,600)



    win.show()

    #a = QMessageBox()
    #a.setText("Hello!")
    #a.show()

    app.exec()