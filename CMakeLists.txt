cmake_minimum_required(VERSION 3.23)
project(midi_generator)

add_subdirectory(pybind11)
pybind11_add_module(note SHARED lib/pybind.cpp lib/API.cpp)

target_include_directories(note PRIVATE lib/include ${Boost_INCLUDE_DIR})

add_library(shared_library SHARED lib/API.cpp)
set_target_properties(shared_library PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(shared_library PUBLIC lib/include ${Boost_INCLUDE_DIR})

add_definitions(${Boost_DEFINITIONS})

set_target_properties(shared_library PROPERTIES
        FRAMEWORK TRUE
        FRAMEWORK_VERSION C
        MACOSX_DEPLOYMENT_TARGET 13.0)

set_property(TARGET shared_library PROPERTY CXX_STANDARD 11)

set(CMAKE_CXX_STANDARD 11 CACHE STRING "C++ version selection")  # or 11, 14, 17, 20
set(CMAKE_CXX_STANDARD_REQUIRED ON)  # optional, ensure standard is supported
set(CMAKE_CXX_EXTENSIONS OFF)  # optional, keep compiler extensions off

message(Python3_LIBRARIES)

target_link_libraries(shared_library PUBLIC ${Boost_LIBRARIES} ${Python3_LIBRARIES} pybind11::module pybind11::embed pybind11::lto note)
target_compile_definitions(note PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})
