set(classes
  vtkSlicerLayerDMLogic
)
set(LayerDM_VERSION_MAJOR 1)
set(LayerDM_VERSION_MINOR 1)
set(LayerDM_VERSION_PATCH 0)
set(LayerDM_VERSION "${LayerDM_VERSION_MAJOR}.${LayerDM_VERSION_MINOR}.${LayerDM_VERSION_PATCH}")

configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/vtkSlicerLayerDMVersion.h.in"
  "${CMAKE_CURRENT_BINARY_DIR}/vtkSlicerLayerDMVersion.h"
  @ONLY
)

set(headers
  "${CMAKE_CURRENT_BINARY_DIR}/vtkSlicerLayerDMVersion.h"
)

vtk_module_add_module(SlicerLayerDM::Logic
  EXPORT_MACRO_PREFIX VTK_SLICER_LAYERDM_MODULE_LOGIC
  CLASSES ${classes}
  HEADERS ${headers}
)
