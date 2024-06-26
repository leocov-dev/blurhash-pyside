//
// Created by Leonardo Covarrubias on 6/23/24.
//

#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/string_view.h>
#include <nanobind/stl/string.h>
#include <blurhash-cpp/blurhash.hpp>
#include <utility>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)


namespace py = nanobind;
using namespace py::literals;

uint8_t bytesPerChannel = 4;

using IntVector = std::vector<uint8_t>;
using String = std::string_view;

NB_MODULE(_core, m) {

    m.def("decode", [](String blurhash, size_t width, size_t height) {
              blurhash::Image img = blurhash::decode(
                      blurhash,
                      width, height,
                      bytesPerChannel
              );
              return img.image;
          },
          "blurhash"_a,
          "width"_a, "height"_a
    );

    m.def("encode", [](
                  IntVector image,
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
          "image"_a,
          "width"_a, "height"_a,
          "components_x"_a, "components_y"_a
    );

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
