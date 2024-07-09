cmake_minimum_required(VERSION 3.27)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -fvisibility=hidden")
set(MACOSX_DEPLOYMENT_TARGET 11)
if (DEFINED SKBUILD_PROJECT_VERSION)
    set(VERSION ${SKBUILD_PROJECT_VERSION})
else ()
    set(VERSION "dev")
endif ()
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif ()

# define project
project(blurhash-pyside
        LANGUAGES CXX)

# cmake finds python
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

message("SOABI: ${Python_SOABI}")

# Detect the installed pybind package and import it into CMake
execute_process(
        COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
        OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE PYB_DIR)
list(APPEND CMAKE_PREFIX_PATH "${PYB_DIR}")
find_package(pybind11 CONFIG REQUIRED)

# Add `extern` dependencies
add_subdirectory(extern/blurhash-cpp)

# Configure Module
pybind11_add_module(_core MODULE src/wrapper.cpp)
target_link_libraries(_core PRIVATE
        blurhash-cpp
)

# pass version into cpp module
target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})

# install the module binary, scikit will put this in the venv when in local dev mode
install(TARGETS _core DESTINATION blurhash_pyside)
