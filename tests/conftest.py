from pathlib import Path

import cv2
import numpy as np
import pytest
from skimage.metrics import structural_similarity

from blurhash_pyside._qt import QImage

_tests_data_dir = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def test_data():
    return _tests_data_dir


def _qimage_to_cv_mat(img: QImage) -> cv2.Mat:
    rgb32 = img.convertToFormat(QImage.Format.Format_RGB32)
    arr = np.array(rgb32.constBits(), copy=True).reshape(rgb32.height(), rgb32.width(), 4)
    return cv2.cvtColor(arr, cv2.COLOR_BGRA2RGB)


def assert_qimages_equal(img_a: QImage, img_b: QImage, tolerance: float = 0.001) -> None:
    view_a = _qimage_to_cv_mat(img_a)
    view_b = _qimage_to_cv_mat(img_b)

    score = structural_similarity(view_a, view_b, data_range=255, channel_axis=2)

    if 1.0 - score > tolerance:
        pytest.fail(f"ssim score failed with value: {score:8f}")
