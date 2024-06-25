from pathlib import Path

import pytest

_tests_data_dir = Path(__file__).parent / 'data'


@pytest.fixture(scope='session')
def test_data():
    return _tests_data_dir
