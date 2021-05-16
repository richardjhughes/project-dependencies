cmake_minimum_required(VERSION 3.15)

project(sqlite3 C)

add_library("${PROJECT_NAME}" INTERFACE)
add_library("${PROJECT_NAME}::${PROJECT_NAME}" ALIAS "${PROJECT_NAME}")

target_sources(
    "${PROJECT_NAME}"
    PUBLIC INTERFACE
        include/sqlite3.h
        include/sqlite3ext.h
    PRIVATE INTERFACE
        src/sqlite3.c
)

# 2021-05-16 - ignore the warnings sqlite3 currently has
target_compile_options(
    "${PROJECT_NAME}"
    PUBLIC INTERFACE
        "-Wno-unused-parameter"
        "-Wno-missing-field-initializers"
        "-Wno-sign-compare"
)

target_include_directories(
    ${PROJECT_NAME}
    INTERFACE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}>
        $<INSTALL_INTERFACE:include>
)

set("SQLITE_PROJECT_NAME" "${PROJECT_NAME}" CACHE INTERNAL "SQLITE_PROJECT_NAME")