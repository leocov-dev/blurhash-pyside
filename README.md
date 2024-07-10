# blurhash-pyside

![GitHub License](https://img.shields.io/github/license/leocov-dev/blurhash-pyside)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/leocov-dev/blurhash-pyside/ci.yml)
![GitHub Release](https://img.shields.io/github/v/release/leocov-dev/blurhash-pyside)
![PyPI - Version](https://img.shields.io/pypi/v/blurhash-pyside)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/blurhash-pyside)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/blurhash-pyside)


Blurhash encoding and decoding for PySide2/6. 
This is a lightweight wrapper using the C++ encoding and decoding functions 
provided by [Nheko-Reborn/blurhash](https://github.com/Nheko-Reborn/blurhash).

- Encode a QImage or QPixmap into a blurhash string
- Decode a blruhash string into a QImage or QPixmap

For more information about Blurhash visit their [official page](https://blurha.sh/).

## Dependencies

This project has no external dependencies other than that you must provide 
either PySide2 or PySide6 in your own project.

The library is pre-compiled for popular platforms and recent Python versions. 
See the [Releases](https://github.com/leocov-dev/blurhash-pyside/releases) or [PyPi](https://pypi.org/project/blurhash-pyside/) page for available wheels.

## Local Development

Requirements:
- Python 3.9+
- Hatch
- CMake 3.27+

Run the example:
```shell
# choose one:
hatch run pyside6:example

# pyside2 may not be available for all python versions or platforms
hatch run pyside2:example
```

### Setup your local environment

Create a repo relative `.venv/` dir:
```shell
hatch env create
```

Run the tests:
```shell
hatch test
```

Build the wheel for your platform:
```shell
hatch build -t wheel
```

Recompile the C++ project:
```shell
hatch run compile
```

The `cmake` project is not intended to be run on its own but it is possible to do it.
The `pybind11` dependency will be available after creating the default virtual environment
and passing its python executable path to `cmake` via `Python_EXECUTABLE`. Some IDE's may
do this for you when a python environment is activated in their configuration.

Manual CMake build
```shell
cmake -S . -B cmake-build-release -G Ninja
cmake --build cmake-build-release -j 8
cmake --install cmake-build-release --prefix src
```

## Acknowledgements

The core C++ code for the blurhash functions was source from https://github.com/Nheko-Reborn/blurhash
under the Boost Software License. Some minor [modifications](extern/blurhash-cpp/README.md) were made.

This project is made possible by [pybind11](https://github.com/pybind/pybind11) and [scikit-build-core](https://github.com/scikit-build/scikit-build-core). 
Multi-platform wheels are generated using the [cibuildwheel](https://github.com/pypa/cibuildwheel) project.
