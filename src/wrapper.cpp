#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/iostream.h>
#include <utility>
#include "blurhash-cpp/blurhash.hpp"


namespace py = pybind11;
using namespace py::literals;

// for wrapper we don't allow specifying bpp, always use 4 with white/255 alpha channel
uint8_t bytesPerChannel = 4;

PYBIND11_MODULE(_core, m) {

    using IntVector = std::vector<uint8_t>;
    using String = std::string_view;

    m.def("decode", [](String blurhash, int width, int height) {
              py::scoped_ostream_redirect stream(
                      std::cout, py::module_::import("sys").attr("stdout"));
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
                  int width, int height,
                  int components_x, int components_y
          ) {
              py::scoped_ostream_redirect stream(
                      std::cout, py::module_::import("sys").attr("stdout"));
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
}
