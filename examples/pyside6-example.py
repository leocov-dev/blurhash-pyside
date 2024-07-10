import sys

from demo import launch_demo
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication()

    _ = launch_demo("PySide2 Blurhash Example")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
