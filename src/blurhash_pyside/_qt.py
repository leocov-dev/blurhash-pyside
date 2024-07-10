_failed_pyside6 = False
_failed_pyside2 = False

try:
    from PySide6.QtCore import QSize, Qt
    from PySide6.QtGui import QImage, QPixmap
except ImportError:
    _failed_pyside6 = True

try:
    from PySide2.QtCore import QSize, Qt
    from PySide2.QtGui import QImage, QPixmap
except ImportError:
    _failed_pyside2 = True

if _failed_pyside6 and _failed_pyside2:
    raise ImportError("Could not import PySide6 or PySide2")

__all__ = [
    "QSize",
    "Qt",
    "QImage",
    "QPixmap",
]
