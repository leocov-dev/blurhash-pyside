from __future__ import annotations

from qtpy.QtCore import QMimeData, Qt, Signal
from qtpy.QtGui import QDragEnterEvent, QDropEvent, QFontMetrics, QImage, QPainter, QPaintEvent, QPalette, QPen, QPixmap
from qtpy.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from blurhash_pyside import Components, decode_to_qpixmap, encode_qpixmap, errors


class ImgPreview(QWidget):
    """Preview an image or show placeholder text if no image"""

    def __init__(self, placeholder_text: str, parent: QWidget):
        super().__init__(parent=parent)

        self._placeholder_text = placeholder_text
        self._pix: QPixmap | None = None

    def setPixmap(self, pix: QPixmap | None):
        self._pix = pix
        self.update()

    @property
    def pixmap_sized(self):
        if not self._pix:
            return None
        return self._pix.scaled(
            self.rect().size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        )

    def clear(self):
        self.setPixmap(None)

    def paintEvent(self, event: QPaintEvent):
        p = QPainter(self)
        p.setClipRect(self.rect())
        if self._pix:
            pix = self.pixmap_sized
            p.drawPixmap((self.rect().width() - pix.width()) // 2, 0, pix)
        else:
            p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
            p.setPen(QPen(self.palette().color(QPalette.ColorRole.Text)))
            p.setFont(self.font())
            fm = QFontMetrics(self.font())
            text_rect = fm.boundingRect(self.rect(), Qt.AlignmentFlag.AlignCenter, self._placeholder_text)
            p.drawText(text_rect, self._placeholder_text)

            pen = QPen(self.palette().color(QPalette.ColorRole.Window))
            pen.setWidth(4)
            p.setPen(pen)
            p.drawRect(self.rect())
        p.end()
        event.accept()


class ComponentsEditor(QWidget):
    """edit x/y blurhash components"""

    value_changed = Signal(object)

    def __init__(self, x: int, y: int, parent=QWidget):
        super().__init__(parent=parent)

        _ly = QHBoxLayout()
        _ly.setContentsMargins(0, 0, 0, 0)
        self.setLayout(_ly)

        _ly.addWidget(QLabel("Components"), alignment=Qt.AlignmentFlag.AlignRight, stretch=4)

        self._x = QSpinBox(parent=self)
        self._x.setRange(1, 9)
        self._x.setValue(x)
        _ly.addWidget(self._x, stretch=2)

        self._y = QSpinBox(parent=self)
        self._y.setRange(1, 9)
        self._y.setValue(y)
        _ly.addWidget(self._y, stretch=2)

        # ---
        self._x.valueChanged.connect(lambda: self.value_changed.emit(self.components))
        self._y.valueChanged.connect(lambda: self.value_changed.emit(self.components))

    @property
    def components(self) -> Components:
        return Components(self._x.value(), self._y.value())


class EncodeDemo(QWidget):
    """demonstrate blurhash encoding"""

    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)

        _ly = QVBoxLayout()
        _ly.setSpacing(3)
        self.setLayout(_ly)

        self._orig = ImgPreview("Drag Image to Encode Here", parent=self)
        _ly.addWidget(self._orig, stretch=9)

        _ly_bhs = QHBoxLayout()
        _ly_bhs.setContentsMargins(0, 0, 0, 0)
        _ly.addLayout(_ly_bhs, stretch=1)

        self._bh_string = QLineEdit(parent=self)
        self._bh_string.setReadOnly(True)
        self._bh_string.setPlaceholderText("Encoded Blurhash String...")
        _ly_bhs.addWidget(self._bh_string)

        self._copy = QPushButton("Copy", parent=self)
        _ly_bhs.addWidget(self._copy)

        self._clear = QPushButton("Clear", parent=self)
        _ly_bhs.addWidget(self._clear)

        self._components = ComponentsEditor(4, 3, parent=self)
        _ly.addWidget(self._components, stretch=1)

        self._encoded = ImgPreview("Preview", parent=self)
        _ly.addWidget(self._encoded, stretch=9)

        # ---
        self._copy.clicked.connect(lambda: QApplication.clipboard().setText(self._bh_string.text()))

        self._clear.clicked.connect(lambda: self._orig.clear())
        self._clear.clicked.connect(lambda: self._encoded.clear())
        self._clear.clicked.connect(lambda: self._bh_string.clear())

        self._components.value_changed.connect(lambda: self._update_blurhash())

    def dragEnterEvent(self, event: QDragEnterEvent):
        img = self._img_from_mimeData(event.mimeData())
        if img:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        img = self._img_from_mimeData(event.mimeData())
        if img:
            self._orig.setPixmap(QPixmap.fromImage(img))
            self._update_blurhash()
            event.accept()
        else:
            event.ignore()

    def _update_blurhash(self):
        if not self._orig.pixmap_sized:
            return

        str_val = encode_qpixmap(self._orig.pixmap_sized, self._components.components)
        self._bh_string.setText(str_val)
        self._encoded.setPixmap(
            decode_to_qpixmap(str_val, self._orig.pixmap_sized.width(), self._orig.pixmap_sized.height())
        )

    def _img_from_mimeData(self, mime_data: QMimeData) -> QImage | None:
        try:
            img = QImage(mime_data.urls()[0].toLocalFile())
            if img.constBits():
                return img
        except:
            pass
        return None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_blurhash()


class DecodeDemo(QWidget):
    """demonstrate blurhash decoding"""

    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)

        _ly = QVBoxLayout()
        _ly.setSpacing(3)
        self.setLayout(_ly)

        _ly_bhs = QHBoxLayout()
        _ly_bhs.setContentsMargins(0, 0, 0, 0)
        _ly.addLayout(_ly_bhs, stretch=1)

        self._bh_string = QLineEdit(parent=self)
        self._bh_string.setPlaceholderText("Enter Encoded Blurhash String Here")
        _ly_bhs.addWidget(self._bh_string)

        self._clear = QPushButton("Clear", parent=self)
        _ly_bhs.addWidget(self._clear)

        self._decoded = ImgPreview("Decoded", parent=self)
        _ly.addWidget(self._decoded, stretch=9)

        # ----
        self._bh_string.textChanged.connect(lambda: self._update_blurhash())

        self._clear.clicked.connect(lambda: self._bh_string.clear())

    def _update_blurhash(self):
        if not self._bh_string.text():
            self._decoded.clear()
            return

        try:
            decoded = decode_to_qpixmap(self._bh_string.text(), self._decoded.width(), self._decoded.height())
            if decoded:
                self._decoded.setPixmap(decoded)
        except errors.BlurhashDecodingError:
            pix = QPixmap(32, 32)
            pix.fill("red")
            # TODO: better error pixmap? draw X or msg text?
            self._decoded.setPixmap(pix)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_blurhash()


class BlurhashDemo(QWidget):
    """demo for blurhash encoding and decoding in 2 tabs"""

    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.setMinimumSize(480, 480)

        _ly = QVBoxLayout()
        self.setLayout(_ly)

        self._tabs = QTabWidget(parent=self)
        _ly.addWidget(self._tabs)

        self._encode = EncodeDemo(parent=self)
        self._tabs.addTab(self._encode, "Encode Demo")

        self._decode = DecodeDemo(parent=self)
        self._tabs.addTab(self._decode, "Decode Demo")
