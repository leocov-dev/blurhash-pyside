import pytest
from conftest import assert_qimages_equal

from blurhash_pyside import decode_to_qimage
from blurhash_pyside._qt import QImage
from blurhash_pyside.errors import BlurhashDecodingError


def test_decode__qimage(test_data):
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


@pytest.mark.parametrize(
    "blurhash_string",
    [
        "",
        " ",
        "ABC",
        "aghwmepjiSJDSFapispidfu",
    ],
)
def test_decode__bad_string(blurhash_string: str):
    with pytest.raises(BlurhashDecodingError):
        decode_to_qimage(
            blurhash_string,
            64,
            64,
        )


def test_decode__bad_size():
    with pytest.raises(BlurhashDecodingError):
        decode_to_qimage("LGFO~6Yk^6#M@-5c,1Ex@@or[j6o", 0, 0)
