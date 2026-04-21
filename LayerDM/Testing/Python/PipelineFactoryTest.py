from unittest.mock import MagicMock

import slicer
from slicer import (
    vtkMRMLLayerDMPipelineFactory,
    vtkMRMLLayerDMPipelineCreatorI
)
from slicer.ScriptedLoadableModule import ScriptedLoadableModuleTest
from vtk import vtkCommand


class PipelineFactoryTest(ScriptedLoadableModuleTest):
    def setUp(self):
        slicer.mrmlScene.Clear(0)
        self.factory = vtkMRMLLayerDMPipelineFactory()

    def test_provides_singleton_instance(self):
        assert vtkMRMLLayerDMPipelineFactory.GetInstance() == vtkMRMLLayerDMPipelineFactory.GetInstance()

    def test_can_remove_creator_by_ref(self):
        c1 = vtkMRMLLayerDMPipelineCreatorI()

        self.factory.AddPipelineCreator(c1)
        assert self.factory.ContainsPipelineCreator(c1)

        c2 = vtkMRMLLayerDMPipelineCreatorI()
        assert not self.factory.ContainsPipelineCreator(c2)
        self.factory.AddPipelineCreator(c2)
        assert self.factory.ContainsPipelineCreator(c2)

        self.factory.RemovePipelineCreator(c1)
        assert not self.factory.ContainsPipelineCreator(c1)

    def test_invokes_modified_event_on_add_remove_creator(self):
        creator = vtkMRMLLayerDMPipelineCreatorI()
        mock = MagicMock()
        self.factory.AddObserver(vtkCommand.ModifiedEvent, mock)

        self.factory.AddPipelineCreator(creator)
        mock.assert_called_once()
        mock.reset_mock()

        self.factory.RemovePipelineCreator(creator)
        mock.assert_called_once()
        mock.reset_mock()

        self.factory.RemovePipelineCreator(creator)
        mock.assert_not_called()
