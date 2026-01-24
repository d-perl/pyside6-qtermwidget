cmake_minimum_required(VERSION 3.16)
project(qtermwidget_python_bindings)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

# Set paths for external libraries
set(EXT_QTERMWIDGET_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external/qtermwidget")
set(EXT_LXQT_BUILD_TOOLS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external/lxqt-build-tools")

# QTermWidget install
set(QTERMWIDGET_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../qtermwidget/build/install")

# Shiboken
execute_process(
    COMMAND python3 -c "from pathlib import Path; import shiboken6; print(Path(shiboken6.__file__).parent / 'include')"
    OUTPUT_VARIABLE SHIBOKEN_INCLUDE
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Shiboken generator
execute_process(
    COMMAND python3 -c "from pathlib import Path; import shiboken6_generator; print(Path(shiboken6_generator.__file__).parent / 'include')"
    OUTPUT_VARIABLE SHIBOKEN_GENERATOR_INCLUDE
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# PySide
execute_process(
    COMMAND python3 -c "from pathlib import Path; import PySide6; print(Path(PySide6.__file__).parent / 'include')"
    OUTPUT_VARIABLE PYSIDE_INCLUDE
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Python include 
execute_process(
    COMMAND python3 -c "import sysconfig; print(sysconfig.get_path('include'))"
    OUTPUT_VARIABLE PYTHON_INCLUDE
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

message(STATUS "Shiboken include: ${SHIBOKEN_INCLUDE}")
message(STATUS "Shiboken Generator include: ${SHIBOKEN_GENERATOR_INCLUDE}")
message(STATUS "PySide include: ${PYSIDE_INCLUDE}")
message(STATUS "qtermwidget include: ${EXT_QTERMWIDGET_DIR}/lib")

# print 'ls' of the qtermwidget lib directory for debugging
execute_process(
    COMMAND ls -l ${QTERMWIDGET_DIR}/include/qtermwidget6
    OUTPUT_VARIABLE QTERMWIDGET_INCLUDE_CONTENTS
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
message(STATUS "Contents of qtermwidget include directory:\n${QTERMWIDGET_INCLUDE_CONTENTS}")

# Shiboken-generated sources
set(SHIBOKEN_SOURCES
    build_bindings/qtermwidget/qtermwidget_module_wrapper.cpp
    build_bindings/qtermwidget/qtermwidget_wrapper.cpp
)

# Build the Python extension 
add_library(_qtermwidget MODULE ${SHIBOKEN_SOURCES})

# Includes 
target_include_directories(_qtermwidget PRIVATE
    ${SHIBOKEN_INCLUDE}
    ${SHIBOKEN_GENERATOR_INCLUDE}
    ${PYSIDE_INCLUDE}
    ${PYSIDE_INCLUDE}/QtCore
    ${PYSIDE_INCLUDE}/QtGui
    ${PYSIDE_INCLUDE}/QtWidgets
    ${PYTHON_INCLUDE}
    ${CMAKE_CURRENT_SOURCE_DIR}/build_bindings/qtermwidget
    ${QTERMWIDGET_DIR}/include
    ${QTERMWIDGET_DIR}/include/qtermwidget6
    # ${EXT_QTERMWIDGET_DIR}/lib
    # ${EXT_LXQT_BUILD_TOOLS_DIR}/include
)


# Link libraries
if (APPLE)
    # Get the path to the Shiboken and PySide dylibs for macOS
    execute_process(
        COMMAND python3 -c "from pathlib import Path; import shiboken6; print(Path(shiboken6.__file__).parent)"
        OUTPUT_VARIABLE SHIBOKEN_DYLIB_PATH
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    # Find the correct dylib for shiboken6 (e.g., libshiboken6.abi3.6.9.dylib)
    file(GLOB SHIBOKEN_DYLIBS "${SHIBOKEN_DYLIB_PATH}/libshiboken6*.dylib")
    list(GET SHIBOKEN_DYLIBS 0 SHIBOKEN_DYLIB_PATH)  # Take the first match

    message(STATUS "Using Shiboken dylib: ${SHIBOKEN_DYLIB_PATH}")

    # Get the path to the PySide dylib for macOS
    execute_process(
        COMMAND python3 -c "from pathlib import Path; import PySide6; print(Path(PySide6.__file__).parent)"
        OUTPUT_VARIABLE PYSIDE_DYLIB_PATH
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    # Find the correct dylib for PySide6 (e.g., libpyside6.abi3.6.9.dylib)
    file(GLOB PYSIDE_DYLIBS "${PYSIDE_DYLIB_PATH}/libpyside6*.dylib")
    list(GET PYSIDE_DYLIBS 0 PYSIDE_DYLIB_PATH)  # Take the first match

    message(STATUS "Using PySide dylib: ${PYSIDE_DYLIB_PATH}")

    target_link_libraries(_qtermwidget
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        ${QTERMWIDGET_DIR}/lib/libqtermwidget6.dylib
        Python3::Python
        ${SHIBOKEN_DYLIB_PATH}
        ${PYSIDE_DYLIB_PATH}
    )
else ()
    target_link_libraries(_qtermwidget
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        ${QTERMWIDGET_DIR}/lib/libqtermwidget6.so
    )
endif()

# RPATH so it finds libqtermwidget6.so in the same folder
set_target_properties(_qtermwidget PROPERTIES
    PREFIX ""
    OUTPUT_NAME "_qtermwidget"
    INSTALL_RPATH "$ORIGIN"
)