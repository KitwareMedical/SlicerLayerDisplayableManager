set(classes
  vtkMRMLLayerDMNodeReferenceObserver
  vtkMRMLLayerDMObjectEventObserver
  vtkMRMLLayerDMWidgetEventTranslationNode
  vtkMRMLLayerDMSelectionObserver
)

if (VTK_WRAP_PYTHON)
  list(APPEND classes
    vtkMRMLLayerDMObjectEventObserverScripted
    vtkMRMLLayerDMPythonUtil
  )
endif ()


vtk_module_add_module(VTK::SlicerLayerDMModuleMRML
  EXPORT_MACRO_PREFIX VTK_SLICER_LAYERDM_MODULE_MRML
  CLASSES ${classes}
)
