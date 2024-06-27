import sys

from demo.blurhash_widget import BlurhashDemo
from PySide6.QtWidgets import QApplication, QMainWindow


def main():
    app = QApplication()

    main_window = QMainWindow()
    main_window.setWindowTitle("PySide6 Blurhash Example")
    main_window.setCentralWidget(BlurhashDemo(parent=main_window))
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
