set(classes vtkMRMLDummyLayerDMPipeline)

vtk_module_add_module(Dummy::MRMLLayerDMPipeline
  EXPORT_MACRO_PREFIX VTK_DUMMY_MRMLLAYERDMPIPELINE
  CLASSES ${classes}
)
