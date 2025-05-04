from PySide6.QtWidgets import QApplication,QMessageBox,QLabel
from PySide6.QtGui import QPixmap,QImage
from main_window import MainWindow


if __name__ == "__main__":
    app = QApplication()
    img:QPixmap = QPixmap()
    img.load("icon.png")
    app.setWindowIcon(img)
    win = MainWindow()
    win.setWindowTitle("LiveSmarter")
    win.resize(800,500)



    win.show()

    #a = QMessageBox()
    #a.setText("Hello!")
    #a.show()

    app.exec()