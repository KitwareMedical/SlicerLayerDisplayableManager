from unittest.mock import MagicMock
import tempfile
from pathlib import Path

import slicer
from slicer.ScriptedLoadableModule import ScriptedLoadableModuleTest
from LayerDMLib import vtkMRMLNodeScripted, NodeProperty
from vtkmodules.vtkCommonCore import vtkCommand


class MyBaseMRMLNode(vtkMRMLNodeScripted):
    float_val: float = NodeProperty()
    bool_val: bool = NodeProperty()
    string_val: str = NodeProperty()
    int_val: int = NodeProperty()
    dict_val: dict[str, float] = NodeProperty()


class MyDerivedMRMLNode(MyBaseMRMLNode):
    derived_val: int = NodeProperty()


class MRMLNodeScriptedTest(ScriptedLoadableModuleTest):
    def setUp(self):
        slicer.mrmlScene.Clear(0)

        MyBaseMRMLNode.RegisterInScene()
        MyDerivedMRMLNode.RegisterInScene()

    def test_can_be_registered_in_the_mrml_scene(self):
        node1 = slicer.mrmlScene.AddNewNodeByClass("MyBaseMRMLNode")
        assert node1 is not None
        assert isinstance(node1, MyBaseMRMLNode)

        node2 = slicer.mrmlScene.AddNewNodeByClass("MyDerivedMRMLNode")
        assert node2 is not None
        assert isinstance(node2, MyDerivedMRMLNode)

    def test_can_be_accessed_from_the_scene(self):
        node = MyDerivedMRMLNode()
        node.float_val = 1.2
        node.bool_val = True
        node.string_val = "test_string"
        node.int_val = 42
        node.derived_val = 3
        node.dict_val = {"a": 42.0}

        node = slicer.mrmlScene.AddNode(node)
        node_id = node.GetID()

        retrieved_node = slicer.mrmlScene.GetNodeByID(node_id)
        assert retrieved_node is not None

        assert retrieved_node.float_val == 1.2
        assert retrieved_node.bool_val
        assert retrieved_node.string_val == "test_string"
        assert retrieved_node.int_val == 42
        assert retrieved_node.derived_val == 3
        assert retrieved_node.dict_val == {"a": 42.0}

    def test_can_be_saved_and_restored_from_mrml(self):
        node = MyDerivedMRMLNode()
        node.int_val = 1
        node.float_val = 1.2
        node.string_val = "a_string"
        node.bool_val = True
        node.derived_val = 3
        node.dict_val = {"a": 42.0}

        node = slicer.mrmlScene.AddNode(node)
        node_id = node.GetID()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_scene_path = Path(temp_dir) / "test_scene.mrml"
            slicer.util.saveScene(temp_scene_path.as_posix())
            assert temp_scene_path.exists()

            slicer.mrmlScene.Clear(0)
            slicer.util.loadScene(temp_scene_path.as_posix())

            retrieved_node = slicer.mrmlScene.GetNodeByID(node_id)
            assert retrieved_node is not None

            assert retrieved_node.int_val == 1
            assert retrieved_node.float_val == 1.2
            assert retrieved_node.string_val == "a_string"
            assert retrieved_node.bool_val
            assert retrieved_node.derived_val == 3
            assert retrieved_node.dict_val == {"a": 42.0}

    def test_triggers_modified_on_field_change(self):
        mock = MagicMock()

        node = slicer.mrmlScene.AddNewNodeByClass("MyDerivedMRMLNode")
        node.AddObserver(vtkCommand.ModifiedEvent, mock)
        node.float_val = 12.0
        mock.assert_called_once()
