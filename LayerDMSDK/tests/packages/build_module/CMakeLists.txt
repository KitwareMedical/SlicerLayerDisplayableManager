cmake_minimum_required(VERSION 3.17...4.0)

project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

find_package(SlicerLayerDM CONFIG REQUIRED)

include(VTKSDKPythonWheelHelper)

# Install runtime only dependencies
vtksdk_build_modules(${SKBUILD_PROJECT_NAME}
  MODULES Dummy::MRMLLayerDMPipeline
  DEPENDENCIES slicer_layer_dm
)
vtksdk_generate_package_init(${SKBUILD_PROJECT_NAME}
  MODULES Dummy::MRMLLayerDMPipeline
  DEPENDENCIES slicer_layer_dm
)

# Make this package part of the slicer meta package
install(FILES
  ${CMAKE_SOURCE_DIR}/Python/slicer_layer_dm_pipeline.py
  DESTINATION slicer
)
