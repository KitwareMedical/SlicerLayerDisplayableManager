set(classes
  vtkSlicerLayerDMLogic
)

# COPY / PASTED from module CMakeLists
set(MODULE_NAME LayerDM)
set(${MODULE_NAME}_VERSION_MAJOR 1)
set(${MODULE_NAME}_VERSION_MINOR 0)
set(${MODULE_NAME}_VERSION_PATCH 0)
set(${MODULE_NAME}_VERSION "${${MODULE_NAME}_VERSION_MAJOR}.${${MODULE_NAME}_VERSION_MINOR}.${${MODULE_NAME}_VERSION_PATCH}")

configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/vtkSlicerLayerDMVersion.h.in"
  "${CMAKE_CURRENT_BINARY_DIR}/vtkSlicerLayerDMVersion.h"
  @ONLY
)

set(headers
  "${CMAKE_CURRENT_BINARY_DIR}/vtkSlicerLayerDMVersion.h"
)

vtk_module_add_module(VTK::SlicerLayerDMModuleLogic
  EXPORT_MACRO_PREFIX VTK_SLICER_LAYERDM_MODULE_LOGIC
  CLASSES ${classes}
  HEADERS ${headers}
)
