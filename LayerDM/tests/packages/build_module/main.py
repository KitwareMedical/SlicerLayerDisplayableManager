# This tests that we can use our custom vtkMRMLLayerDMPipelineI subclass
# with the vtkMRMLLayerDMPipelineScriptedCreator and vtkMRMLLayerDMPipelineFactory

from slicer import (
    vtkMRMLLayerDMPipelineFactory,
    vtkMRMLDummyLayerDMPipeline,
    vtkMRMLLayerDMPipelineScriptedCreator
)


factory = vtkMRMLLayerDMPipelineFactory()
creator = vtkMRMLLayerDMPipelineScriptedCreator()
creator.SetPythonCallback(lambda *_ : vtkMRMLDummyLayerDMPipeline())
factory.AddPipelineCreator(creator)
assert(isinstance(factory.CreatePipeline(None, None), vtkMRMLDummyLayerDMPipeline))
