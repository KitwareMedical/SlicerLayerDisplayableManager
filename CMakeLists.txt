# CMake will complain if this is not in this file specifically
cmake_minimum_required(VERSION 3.16.3...4.0)

# Most CMakeLists.txt files in this repo will have this conditional structure
# SlicerLayerDM can be built in two different ways:
# - A 3DSlicer extension
# - A slicer-core based python wheel
# Using include like this enables the CMake code to be in the expected
# source/binary directory and add_subdirectory to work seamlessly
if(DEFINED SKBUILD_PROJECT_NAME)
  project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})
  include(${CMAKE_CURRENT_SOURCE_DIR}/wheel.cmake)
else()
  project(LayerDisplayableManager)

  # disable https://cmake.org/cmake/help/latest/policy/CMP0148.html as vtkAddon may need it
  if(POLICY CMP0148)
    cmake_policy(SET CMP0148 OLD)
  endif()

  include(${CMAKE_CURRENT_SOURCE_DIR}/extension.cmake)
endif()
