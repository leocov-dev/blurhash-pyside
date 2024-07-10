from typing import NamedTuple

from ._core import decode, encode
from ._qt import QImage, QPixmap, QSize, Qt
from .errors import BlurhashDecodingError, BlurhashEncodingError


def decode_to_qimage(blurhash: str, width: int, height: int) -> QImage:
    """
    Decode a Blurhash string to a QImage.
    """
    try:
        data = decode(blurhash.strip(), width, height)
    except Exception as e:
        raise BlurhashDecodingError(str(e)) from e

    if len(data) < height * width * 4:
        raise BlurhashDecodingError("decoded data size did not match expected height/width")

    return QImage(bytes(data), width, height, width * 4, QImage.Format.Format_RGB32).rgbSwapped()


def decode_to_qpixmap(blurhash: str, width: int, height: int) -> QPixmap:
    """
    Decode a Blurhash string to a QPixmap.
    """
    image = decode_to_qimage(blurhash, width, height)
    return QPixmap.fromImage(image)


class Components(NamedTuple):
    x: int
    y: int

    def valid(self) -> bool:
        return 9 >= self.x >= 1 and 9 >= self.y >= 1


def encode_qimage(image: QImage, components: Components, downsample: int = 1) -> str:
    """Encode a QImage to a Blurhash string"""

    if not components.valid():
        raise BlurhashEncodingError(f"Components: {components} invalid")

    image = image.convertToFormat(QImage.Format.Format_RGB32).rgbSwapped()

    if downsample > 1:
        image = image.scaled(
            QSize(downsample, downsample),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation,
        )

    if not image.constBits():
        raise BlurhashEncodingError("QImage to encode seems invalid")

    bpp = 4
    size = image.width() * image.height() * bpp
    data = list(image.constBits())

    ordered = []
    try:
        for i in range(0, size, bpp):
            ordered.extend(data[i : i + bpp][0:3])
    except Exception as e:
        raise BlurhashEncodingError("problem organizing raw image data") from e

    try:
        bh_str = encode(
            ordered,
            image.width(),
            image.height(),
            components.x,
            components.y,
        )
    except Exception as e:
        raise BlurhashEncodingError(str(e)) from e

    if not bh_str:
        raise BlurhashEncodingError("Blurhash result was empty")

    return bh_str


def encode_qpixmap(pixmap: QPixmap, components: Components, downsample_factor: int = 1) -> str:
    """Encode a QPixmap to a Blurhash string"""
    return encode_qimage(pixmap.toImage(), components, downsample_factor)
