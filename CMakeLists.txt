cmake_minimum_required(VERSION 3.27)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(PYBIND11_FINDPYTHON ON)

# define project
project(${SKBUILD_PROJECT_NAME}
        VERSION ${SKBUILD_PROJECT_VERSION}
        LANGUAGES CXX)

# cmake finds python
find_package(Python 3.9 REQUIRED COMPONENTS Interpreter Development.Module)

# Add `extern` dependencies
add_subdirectory(extern/pybind11)
add_subdirectory(extern/blurhash-cpp)

# Configure Module
pybind11_add_module(_core MODULE src/wrapper.cpp)
target_link_libraries(_core PRIVATE
        blurhash-cpp
)

# pass version into cpp module
target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})

# install the module binary, scikit will put this in the venv when in local dev mode
install(TARGETS _core DESTINATION ${SKBUILD_PROJECT_NAME})
