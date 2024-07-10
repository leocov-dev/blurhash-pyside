from pathlib import Path

import pytest

from blurhash_pyside import Components, encode_qimage
from blurhash_pyside._qt import QImage
from blurhash_pyside.errors import BlurhashEncodingError


def test_encode__qimage(test_data: Path):
    img = QImage(str(test_data / "raw.bmp"))
    bh = encode_qimage(img, Components(4, 3))

    assert bh == "LGFO~6Yk^6#M@-5c,1Ex@@or[j6o"


def test_encode__invalid_components(test_data: Path):
    img = QImage(str(test_data / "raw.bmp"))
    with pytest.raises(BlurhashEncodingError):
        encode_qimage(img, Components(0, 0))


def test_encode__invalid_image():
    img = QImage()
    with pytest.raises(BlurhashEncodingError):
        encode_qimage(img, Components(4, 3))
