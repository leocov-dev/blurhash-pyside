from qtpy.QtWidgets import QMainWindow

from .blurhash_widget import BlurhashDemo


def launch_demo(title: str = "Blurhash Demo") -> QMainWindow:
    main_window = QMainWindow()
    main_window.setWindowTitle(title)
    main_window.setCentralWidget(BlurhashDemo(parent=main_window))
    main_window.show()
    return main_window
