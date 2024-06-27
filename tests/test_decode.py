from conftest import assert_qimages_equal
from qtpy.QtGui import QImage

from blurhash_pyside import decode_to_qimage


def test_decode_to_qimage(test_data):
    img = decode_to_qimage(
        "LGFO~6Yk^6#M@-5c,1Ex@@or[j6o",
        301,
        193,
    )

    assert img.constBits()
    assert img.format() == QImage.Format.Format_RGB32
    assert img.width() == 301
    assert img.height() == 193

    assert_qimages_equal(img, QImage(str(test_data / "decoded.png")))
