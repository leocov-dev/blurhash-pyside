from PySide6.QtGui import QImage
from blurhash_pyside import decode_to_qimage


def test_decode__qimage(test_data):
    img = decode_to_qimage(
        "LGFO~6Yk^6#M@-5c,1Ex@@or[j6o",
        301,
        193,
    )

    expected = QImage(str(test_data / "decoded.png"))

    assert img == expected

