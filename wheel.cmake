option(BUILD_SDK "If ON, builds the SDK of the package." OFF)

find_package(Slicer CONFIG REQUIRED)

set(modules
  SlicerLayerDM::Logic
  SlicerLayerDM::MRML
  SlicerLayerDM::MRMLDisplayableManager
)

include(VTKSDKPythonWheelHelper)

set(layout Runtime)
if(BUILD_SDK)
    set(layout SDK)
endif()

vtksdk_build_modules(${SKBUILD_PROJECT_NAME}
  MODULES ${modules}
  DEPENDENCIES slicer_core
  LAYOUT ${layout}
)

if(BUILD_SDK)
  vtksdk_install_modules_sdk(${SKBUILD_PROJECT_NAME}
    MODULES ${modules}
    EXTERNAL_DEPENDENCIES Slicer
  )
else()
  vtksdk_generate_package_init(${SKBUILD_PROJECT_NAME}
    MODULES ${modules}
    DEPENDENCIES slicer_core
  )

  # Make this package part of the slicer meta package
  install(FILES
    ${CMAKE_SOURCE_DIR}/Python/slicer_layer_dm.py
    DESTINATION slicer
  )
endif()
