//
// Created by Leonardo Covarrubias on 6/23/24.
//

#define PYBIND11_DETAILED_ERROR_MESSAGES

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <blurhash-cpp/blurhash.hpp>
#include <utility>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)


namespace py = pybind11;

uint8_t bytesPerChannel = 4;

PYBIND11_MODULE(_core, m) {

    m.def("decode", [](std::string_view blurhash, size_t width, size_t height) {
              blurhash::Image img = blurhash::decode(
                      blurhash,
                      width, height,
                      bytesPerChannel
              );
              return img.image;
          },
          py::arg("blurhash"),
          py::arg("width"),
          py::arg("height")
    );

    m.def("encode", [](
                  std::vector<uint8_t> image,
                  size_t width, size_t height,
                  int components_x, int components_y
          ) {
              return blurhash::encode(
                      image.data(),
                      width, height,
                      components_x, components_y,
                      3
              );
          },
          py::arg("image"),
          py::arg("width"),
          py::arg("height"),
          py::arg("components_x"),
          py::arg("components_y")
    );

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
