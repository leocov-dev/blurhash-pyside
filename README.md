# blurhash-pyside

> 🚧🚧🚧 This is a work in progress until there is a release 🚧🚧🚧

Blurhash encoding and decoding for PySide2/6

- Encode a QImage or QPixmap to a blurhash string
- Decode a blruhash string to a QImage or QPixmap


## Local Development

Requirements:
- Python 3.9+
- Hatch
- CMake 3.27+

Clone the repository with submodules to get the `pybind11` dependency.
```shell
git clone --recursive https://github.com/leocov-dev/blurhash-pyside.git
```

create a project relative `.venv/` dir
```shell
hatch env create
```

run tests
```shell
hatch test
```
