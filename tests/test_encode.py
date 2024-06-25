from pathlib import Path

from qtpy.QtGui import QImage

from blurhash_pyside import Components, encode_qimage


def test_encode__qimage(test_data: Path):
    img = QImage(str(test_data / "raw.bmp"))
    bh = encode_qimage(img, Components(4, 3))

    assert bh == "LGFO~6Yk^6#M@-5c,1Ex@@or[j6o"
