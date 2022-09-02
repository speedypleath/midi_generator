cmake_minimum_required(VERSION 3.23)
project(python_module)

set(CMAKE_SHARED_LIBRARY_PREFIX "")
option(BUILD_SHARED_LIBS "Build using shared libraries" ON)

add_subdirectory(pybind11)
pybind11_add_module(note SHARED lib/pybind.cpp lib/API.cpp)

target_include_directories(note PUBLIC lib/include)

add_library(shared_library SHARED lib/API.cpp)
set_target_properties(shared_library PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(shared_library PUBLIC lib/include)

set_target_properties(shared_library PROPERTIES
        FRAMEWORK TRUE
        FRAMEWORK_VERSION C)

target_link_libraries(shared_library PRIVATE note ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY} ${Boost_LIBRARIES})

target_link_libraries(note PUBLIC ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY} ${Boost_LIBRARIES} pybind11::module pybind11::embed pybind11::lto)
target_compile_definitions(note PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})
