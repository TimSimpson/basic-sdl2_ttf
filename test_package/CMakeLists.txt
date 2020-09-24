cmake_minimum_required(VERSION 3.5)
project(test_package)

set(CMAKE_CXX_STANDARD 17)

find_package(sdl2_ttf)

add_executable(Sdl2TtfSimple WIN32 ${CMAKE_CURRENT_SOURCE_DIR}/Sdl2TtfSimple.cpp)
target_link_libraries(Sdl2TtfSimple PUBLIC sdl2_ttf::sdl2_ttf)
