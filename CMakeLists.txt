cmake_minimum_required(VERSION 3.17...4.0)

project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

find_package(Slicer CONFIG REQUIRED)

include(FetchContent)
FetchContent_Declare(vtk-sdk-python-helper
  GIT_REPOSITORY https://github.com/Kitware/vtk-sdk-python-wheel-helper.git
  GIT_TAG        main
)
FetchContent_MakeAvailable(vtk-sdk-python-helper)

set(modules
  SlicerLayerDM::Logic
  SlicerLayerDM::MRML
  SlicerLayerDM::MRMLDisplayableManager
)

# Install runtime only dependencies
vtksdk_build_modules(${SKBUILD_PROJECT_NAME}
  MODULES ${modules}
  DEPENDENCIES slicer_core
)
vtksdk_generate_package_init(${SKBUILD_PROJECT_NAME}
  MODULES ${modules}
  DEPENDENCIES slicer_core
)

# Make this package part of the slicer meta package
install(FILES
  ${CMAKE_SOURCE_DIR}/Python/slicer_layerdm.py
  DESTINATION slicer
)
