cmake_minimum_required(VERSION 3.15)

project(sqlite3 C)

add_library("${PROJECT_NAME}" INTERFACE)
add_library("${PROJECT_NAME}::${PROJECT_NAME}" ALIAS "${PROJECT_NAME}")

target_sources(
    "${PROJECT_NAME}"
    PUBLIC INTERFACE
        sqlite3.h
        sqlite3ext.h
    PRIVATE INTERFACE
        sqlite3.c
)

target_include_directories(
    ${PROJECT_NAME}
    INTERFACE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}>
        $<INSTALL_INTERFACE:include>
)

set("SQLITE_PROJECT_NAME" "${PROJECT_NAME}" CACHE INTERNAL "SQLITE_PROJECT_NAME")