set(classes
  vtkSlicerLayerDMLogic
)

set(headers
  vtkSlicerLayerDMModuleLogicExport.h
)

vtk_module_add_module(SlicerLayerDM::Logic
  EXPORT_MACRO_PREFIX VTK_SLICER_LAYERDM_MODULE_LOGIC
  CLASSES ${classes}
  HEADERS ${headers}
)
