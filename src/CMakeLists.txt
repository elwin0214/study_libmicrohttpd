cmake_minimum_required(VERSION 3.2)
project(minihttpd)

set(CMAKE_C_COMPILER "gcc")

set(CMAKE_C_FLAGS, "${CMAKE_C_FLAGS} -g -O2 -v")
 
message(WARNING " = " ${PROJECT_SOURCE_DIR})
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR})


add_subdirectory(src/mhttpd)