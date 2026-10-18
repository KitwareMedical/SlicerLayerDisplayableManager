from slicer import vtkSlicerLayerDMLogic, vtkMRMLLayerDMWidgetEventTranslationNode

from LayerDMTestSupport import ScriptedLoadableModuleTest, create_test_scene


class LogicTest(ScriptedLoadableModuleTest):
    def setUp(self):
        self.scene = create_test_scene()

    def test_can_attach_translation_nodes_to_other_nodes(self):
        node = self.scene.AddNewNodeByClass("vtkMRMLModelNode")
        assert node is not None

        tl_node = self.scene.AddNewNodeByClass("vtkMRMLLayerDMWidgetEventTranslationNode")
        assert tl_node is not None

        vtkSlicerLayerDMLogic.SetWidgetEventTranslationNode(node, tl_node)
        assert vtkSlicerLayerDMLogic.GetWidgetEventTranslationNode(node) == tl_node

    def test_can_register_singleton_translation_nodes(self):
        assert vtkSlicerLayerDMLogic.GetWidgetEventTranslationSingleton(self.scene, "MyTLNodeSingleton") is None
        tl_node = vtkSlicerLayerDMLogic.CreateWidgetEventTranslationSingleton(self.scene, "MyTLNodeSingleton")
        assert tl_node is not None
        assert isinstance(tl_node, vtkMRMLLayerDMWidgetEventTranslationNode)
        assert not tl_node.GetSaveWithScene()

    def test_singleton_translation_nodes_are_created_once(self):
        tl_node = vtkSlicerLayerDMLogic.CreateWidgetEventTranslationSingleton(self.scene, "MyTLNodeSingleton")
        assert vtkSlicerLayerDMLogic.CreateWidgetEventTranslationSingleton(self.scene, "MyTLNodeSingleton") == tl_node

    def test_can_attach_singleton_tl_node(self):
        node = self.scene.AddNewNodeByClass("vtkMRMLModelNode")
        assert node is not None
        tl_node = vtkSlicerLayerDMLogic.CreateWidgetEventTranslationSingleton(self.scene, "MyTLNodeSingleton")
        vtkSlicerLayerDMLogic.SetWidgetEventTranslationNode(node, tl_node)
        assert vtkSlicerLayerDMLogic.GetWidgetEventTranslationNode(node) == tl_node
