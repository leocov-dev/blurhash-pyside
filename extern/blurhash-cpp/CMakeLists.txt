cmake_minimum_required(VERSION 3.27)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

project(blurhash-cpp CXX)

add_library(blurhash-cpp "")

target_sources(blurhash-cpp
        PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}/blurhash-cpp/blurhash.cpp
        PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/blurhash-cpp/blurhash.hpp
)

target_include_directories(blurhash-cpp
        PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}
)