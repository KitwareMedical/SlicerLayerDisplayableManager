from slicer import (
    vtkMRMLApplicationLogic,
    vtkMRMLDisplayableManagerGroup,
    vtkMRMLLayerDMPipelineFactory,
    vtkMRMLLayerDMPipeline,
    vtkMRMLLayerDMPipelineManager,
    vtkMRMLLayerDMPipelineScriptedCreator,
    vtkMRMLLayerDisplayableManager,
    vtkMRMLScene,
    vtkMRMLScriptedModuleNode,
    vtkMRMLSliceViewDisplayableManagerFactory,
    vtkMRMLThreeDViewDisplayableManagerFactory,
)
from vtk import VTK_OBJECT, vtkActor, vtkImageData, vtkObjectFactory, vtkRenderer

from LayerDMTestSupport import (
    ScriptedLoadableModuleTest,
    create_render_window,
    create_test_scene,
    is_rendering_supported,
)
from MockPipeline import MockPipeline


class DisplayableManagerTest(ScriptedLoadableModuleTest):
    def setUp(self):
        self.scene = create_test_scene()

        # Verify the DM can be created by the vtk Object Factory
        assert vtkObjectFactory.CreateInstance(vtkMRMLLayerDisplayableManager.__name__) is not None

        # Register the DM to the default views
        vtkMRMLLayerDisplayableManager.RegisterInDefaultViews()

        # Verify registration is correct for both 2D and 3D views
        assert vtkMRMLLayerDisplayableManager.IsRegisteredInFactory(
            vtkMRMLSliceViewDisplayableManagerFactory.GetInstance()
        )
        assert vtkMRMLLayerDisplayableManager.IsRegisteredInFactory(
            vtkMRMLThreeDViewDisplayableManagerFactory.GetInstance()
        )

        # Create a 3D view node and display it in a standalone render window.
        # This is the slicer-core equivalent of the 3D view created by the 3D Slicer
        # application layout manager.
        self.threeDNode = self.scene.AddNewNodeByClass("vtkMRMLViewNode")
        self.renderWindow, self.renderer = create_render_window()

        self.displayableManagerFactory = vtkMRMLThreeDViewDisplayableManagerFactory()
        self.displayableManagerFactory.SetMRMLApplicationLogic(vtkMRMLApplicationLogic())
        vtkMRMLLayerDisplayableManager.RegisterInFactory(self.displayableManagerFactory)

        self.displayableManagerGroup = vtkMRMLDisplayableManagerGroup()
        self.displayableManagerGroup.Initialize(self.displayableManagerFactory, self.renderer)
        self.displayableManagerGroup.SetMRMLDisplayableNode(self.threeDNode)
        self.displayableManager = self.displayableManagerGroup.GetDisplayableManagerByClassName(
            vtkMRMLLayerDisplayableManager.__name__
        )

        self.node = vtkMRMLScriptedModuleNode()

        # Register a pipeline creator with static pipeline
        self.pipeline = MockPipeline()
        self.factory = vtkMRMLLayerDMPipelineFactory.GetInstance()
        self.creator = vtkMRMLLayerDMPipelineScriptedCreator()
        self.creator.SetPythonCallback(
            lambda view, node: self.pipeline if view == self.threeDNode and node == self.node else None
        )
        self.factory.AddPipelineCreator(self.creator)

    def tearDown(self):
        self.factory.RemovePipelineCreator(self.creator)

    def test_registered_pipelines_can_add_their_actors_to_views(self):
        # Configure pipeline renderer added to add a new actor
        actor = vtkActor()

        def onRendererAdded(renderer: vtkRenderer):
            if renderer:
                renderer.AddViewProp(actor)

        self.pipeline.mockOnRendererAdded.side_effect = onRendererAdded

        # Trigger pipeline creation by adding a node to the scene
        self.scene.AddNode(self.node)

        # Verify the pipeline's actor is present in the threed view
        assert self.renderer.HasViewProp(actor)

    def test_registered_pipelines_have_access_to_scene_manager_view_and_display_node(self):
        # Trigger pipeline creation by adding a new model node to the scene
        self.scene.AddNode(self.node)

        # Check getters point to the right instances
        assert self.pipeline.GetScene() == self.scene
        assert isinstance(self.pipeline.GetPipelineManager(), vtkMRMLLayerDMPipelineManager)
        assert self.pipeline.GetViewNode() == self.threeDNode
        assert self.pipeline.GetDisplayNode() == self.node

    def test_registered_pipelines_can_override_setters_to_scene_manager_view_and_display_node(self):
        # Trigger pipeline creation by adding a new model node to the scene
        self.scene.AddNode(self.node)

        # Check overridden setters where called
        self.pipeline.mockSetScene.assert_called_with(self.scene)
        self.pipeline.mockSetPipelineManager.assert_called_with(self.pipeline.GetPipelineManager())
        self.pipeline.mockSetViewNode.assert_called_with(self.threeDNode)
        self.pipeline.mockSetDisplayNode.assert_called_with(self.node)

    def test_pipelines_have_access_to_sibling_pipelines(self):
        # Register a second pipeline creator
        otherNode = vtkMRMLScriptedModuleNode()
        otherPipeline = MockPipeline()

        otherCreator = vtkMRMLLayerDMPipelineScriptedCreator()
        otherCreator.SetPythonCallback(
            lambda view, node: otherPipeline if view == self.threeDNode and node == otherNode else None
        )
        self.factory.AddPipelineCreator(otherCreator)

        # Add both nodes to the scene for pipeline creation to happen
        self.scene.AddNode(self.node)
        self.scene.AddNode(otherNode)

        # Assert the first pipeline has access to the second one
        assert self.pipeline.GetNodePipeline(otherNode) == otherPipeline

    def test_pipelines_can_add_observers_to_vtk_objects_and_events(self):
        def onSetScene(scene: vtkMRMLScene):
            assert self.pipeline.GetScene() != scene
            self.pipeline.UpdateObservation(self.pipeline.GetScene(), scene, vtkMRMLScene.NodeAddedEvent)
            vtkMRMLLayerDMPipeline.SetScene(self.pipeline, scene)

        # Add observer on the scene when its added
        self.pipeline.mockSetScene.side_effect = onSetScene

        self.scene.AddNode(self.node)
        self.pipeline.mockSetScene.assert_called_once()

        modelNode = self.scene.AddNewNodeByClass("vtkMRMLModelNode")
        self.pipeline.mockOnUpdate.assert_called_once()
        args = self.pipeline.mockOnUpdate.call_args[0]
        assert args[0] == self.scene
        assert args[1] == vtkMRMLScene.NodeAddedEvent
        assert self.pipeline.CastCallData(args[2], VTK_OBJECT) == modelNode

    def test_pipelines_update_display_is_called_at_init(self):
        self.scene.AddNode(self.node)
        self.pipeline.mockUpdateFromMRML.assert_called_once()

    def test_pipelines_update_from_mrml_is_called_at_update_display(self):
        self.scene.AddNode(self.node)
        self.pipeline.mockUpdateFromMRML.reset_mock()

        self.pipeline.UpdateDisplay()
        self.pipeline.mockUpdateFromMRML.assert_called_once()

    def test_pipeline_exceptions_are_propagated_to_python(self):
        _error_msg = "Something went wrong in Python"
        self.pipeline.mockUpdateFromMRML.side_effect = RuntimeError(_error_msg)

        with self.assertRaises(RuntimeError) as context:
            self.scene.AddNode(self.node)
        assert _error_msg in str(context.exception)

    def test_can_render_to_image_data(self):
        if not is_rendering_supported():
            self.skipTest("No OpenGL implementation available to render offscreen")

        render_window = self.renderWindow
        render_window.Render()

        # Direct return value call
        image = vtkMRMLLayerDisplayableManager.RenderWindowBufferToImage(render_window)
        assert isinstance(image, vtkImageData)
        assert image.GetDimensions()[0] == render_window.GetSize()[0]
        assert image.GetDimensions()[1] == render_window.GetSize()[1]

        # Mutated call
        image = vtkImageData()
        vtkMRMLLayerDisplayableManager.RenderWindowBufferToImage(render_window, image)
        assert isinstance(image, vtkImageData)
        assert image.GetDimensions()[0] == render_window.GetSize()[0]
        assert image.GetDimensions()[1] == render_window.GetSize()[1]
