cmake_minimum_required(VERSION 3.27)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(PYBIND11_FINDPYTHON ON)
set(MACOSX_DEPLOYMENT_TARGET 12)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# define project
project(${SKBUILD_PROJECT_NAME}
        VERSION ${SKBUILD_PROJECT_VERSION}
        LANGUAGES CXX)

# cmake finds python
find_package(Python 3.9 COMPONENTS Interpreter Development.Module REQUIRED)

# Detect the installed nanobind package and import it into CMake
execute_process(
        COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE NB_DIR)
list(APPEND CMAKE_PREFIX_PATH "${NB_DIR}")
find_package(nanobind CONFIG REQUIRED)

# Add `extern` dependencies
add_subdirectory(extern/blurhash-cpp)

# Configure Module
nanobind_add_module(_core MODULE src/wrapper.cpp)
target_link_libraries(_core PRIVATE
        blurhash-cpp
)

# pass version into cpp module
target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})

# install the module binary, scikit will put this in the venv when in local dev mode
install(TARGETS _core DESTINATION ${SKBUILD_PROJECT_NAME})
