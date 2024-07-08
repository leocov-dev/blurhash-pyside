# Blurhash C++

Original source:
https://github.com/Nheko-Reborn/blurhash

### Modifications

Some modifications were made to the original source code

- raising more exceptions, these are translated by `pybind11` automatically
- adjust some variable types for seamless interop with `pybind11`
- clamp result of `linearToSrgb()` to `0 <= X <= 255`
- minor refactoring
- remove some dead code