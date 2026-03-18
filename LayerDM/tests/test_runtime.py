import pytest


@pytest.mark.runtime
def test_import_layerdm():
    """
    This is a simple test that import the package and checks that it is found.
    """
    from slicer import vtkMRMLLayerDMPipelineI # noqa
    from LayerDMLib import vtkMRMLLayerDMScriptedPipeline

    vtkMRMLLayerDMScriptedPipeline()


@pytest.mark.runtime
def test_layerdm_through_factory():
    """
    Test that we can instantiate a displayable manager using the slicer-core provided factories
    """
    from slicer import (
        vtkMRMLDisplayableManagerGroup,
        vtkMRMLApplicationLogic,
        vtkMRMLLayerDisplayableManager,
        vtkMRMLThreeDViewDisplayableManagerFactory
    )

    from vtkmodules.vtkRenderingCore import (
        vtkRenderer,
        vtkRenderWindow
    )

    factory = vtkMRMLThreeDViewDisplayableManagerFactory()
    factory.SetMRMLApplicationLogic(vtkMRMLApplicationLogic())

    vtkMRMLLayerDisplayableManager.RegisterInFactory(factory)
    assert vtkMRMLLayerDisplayableManager.IsRegisteredInFactory(factory)

    renderer = vtkRenderer()
    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    displayable_manager_group = vtkMRMLDisplayableManagerGroup()
    displayable_manager_group.Initialize(factory, renderer)
    assert displayable_manager_group.GetDisplayableManagerByClassName(vtkMRMLLayerDisplayableManager.__name__)
