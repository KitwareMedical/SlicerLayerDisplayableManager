import sys
from typing import Tuple, Optional

import slicer
import traceback
from LayerDMLib import vtkMRMLLayerDMScriptedPipeline
from slicer import (
    vtkMRMLAbstractViewNode,
    vtkMRMLAbstractWidget,
    vtkMRMLInteractionEventData,
    vtkMRMLLayerDMPipelineFactory,
    vtkMRMLLayerDMPipelineScriptedCreator,
    vtkMRMLLayerDMWidgetEventTranslationNode,
    vtkMRMLNode,
    vtkMRMLScriptedModuleNode,
)
from vtk import vtkCommand, vtkMath


class PrintModelNameDMPipeline(vtkMRMLLayerDMScriptedPipeline):
    """
    The PrintModelNameDMPipeline is a barebone example that prints the model name
    when the mouse hovers or clicks on a model.
    It uses an internal vtkMRMLLayerDMWidgetEventTranslationNode to monitor events.
    """

    creator = None

    def __init__(self):
        super().__init__()

        self._state = vtkMRMLAbstractWidget.WidgetStateIdle
        self.event_enter_widget = vtkMRMLAbstractWidget.WidgetEventUser + 1
        self.event_hover = vtkMRMLAbstractWidget.WidgetEventUser + 2
        self.event_click = vtkMRMLAbstractWidget.WidgetEventUser + 3
        self._modelNode = None

        self._tl_node = vtkMRMLLayerDMWidgetEventTranslationNode()
        self._tl_node.SetSaveWithScene(False)
        self._tl_node.SetHideFromEditors(True)
        self._tl_node.SetTranslation(
            vtkMRMLAbstractWidget.WidgetStateIdle,
            vtkCommand.MouseMoveEvent,
            self.event_enter_widget,
        )

        self._tl_node.SetTranslation(
            vtkMRMLAbstractWidget.WidgetStateOnWidget,
            vtkCommand.MouseMoveEvent,
            self.event_hover,
        )

        self._tl_node.SetTranslation(
            vtkMRMLAbstractWidget.WidgetStateOnWidget,
            vtkCommand.LeftButtonReleaseEvent,
            self.event_hover,
        )

        self._tl_node.SetTranslation(
            vtkMRMLAbstractWidget.WidgetStateOnWidget,
            vtkCommand.LeftButtonPressEvent,
            self.event_click,
        )


    @classmethod
    def CreatePipelineNode(cls, modelNode) -> vtkMRMLScriptedModuleNode:
        if not modelNode:
            return None

        node = vtkMRMLScriptedModuleNode()
        node.SetAttribute("PipelineClass", cls._GetClassName())
        node = slicer.mrmlScene.AddNode(node)
        modelNode.AddNodeReferenceID(f"{cls._GetClassName().lower()}_role", node.GetID())
        return node

    @classmethod
    def IsPipelineNode(cls, node: vtkMRMLNode) -> bool:
        return (
            node is not None
            and node.IsA("vtkMRMLScriptedModuleNode")
            and node.GetAttribute("PipelineClass") == cls._GetClassName()
        )

    @classmethod
    def TryCreatePipeline(
        cls, viewNode: vtkMRMLAbstractViewNode, node: vtkMRMLNode
    ) -> Optional["PrintModelNameDMPipeline"]:
        if not cls.IsPipelineNode(node) or not isinstance(viewNode, slicer.vtkMRMLViewNode):
            return None
        return cls()

    @classmethod
    def _GetClassName(cls) -> str:
        return cls.__name__

    def OnReferenceToDisplayNodeAdded(self, fromNode: Optional[vtkMRMLNode], role: str) -> None:
        self._modelNode = fromNode

    def OnReferenceToDisplayNodeRemoved(self, fromNode: Optional[vtkMRMLNode], role: str) -> None:
        if fromNode == self._modelNode:
            self._modelNode = None

    def CanProcessInteractionEvent(self, eventData: vtkMRMLInteractionEventData) -> Tuple[bool, float]:
        try:
            if not self._IsModelVisible():
                return False, sys.float_info.max

            # Translate event using our internal translation node
            widgetEvent = self._tl_node.Translate(self._state, eventData)
            if widgetEvent == vtkMRMLAbstractWidget.WidgetEventNone:
                return False, sys.float_info.max

            # Check if interaction is within the model's bounding box
            polyData = self._modelNode.GetPolyData()
            pos = [0.0] * 3
            displayPos = [0] * 2
            vtkMRMLLayerDMWidgetEventTranslationNode.GetEventPositions(eventData, pos, displayPos)
            bounds = polyData.GetBounds()
            isInBounds = (
                bounds[0] <= pos[0] <= bounds[1]
                and bounds[2] <= pos[1] <= bounds[3]
                and bounds[4] <= pos[2] <= bounds[5]
            )

            if not isInBounds:
                return False, sys.float_info.max

            distance2 = vtkMath.Distance2BetweenPoints(pos, polyData.GetCenter())
            return True, distance2
        except Exception as e:
            print("Failed to process: ", e)
            traceback.print_exc()
            return False, sys.float_info.max

    def _ResetState(self):
        self._state = vtkMRMLAbstractWidget.WidgetStateIdle

    def ProcessInteractionEvent(self, eventData: vtkMRMLInteractionEventData) -> bool:
        widgetEvent = self._tl_node.Translate(self._state, eventData)
        modelID = self._modelNode.GetID()

        if widgetEvent == self.event_enter_widget:
            self._state = vtkMRMLAbstractWidget.WidgetStateOnWidget
            print(f"Enter widget: {modelID}")
        elif widgetEvent == self.event_click:
            print(f"Click: {modelID}")

        return True

    def _IsModelVisible(self) -> bool:
        if self._modelNode is None or not self._modelNode.GetPolyData():
            return False
        return bool(self._modelNode.GetDisplayVisibility())

    @classmethod
    def RegisterPipeline(cls):
        if cls.creator is not None:
            return

        def tryCreate(view_node, node):
            return PrintModelNameDMPipeline.TryCreatePipeline(view_node, node)

        cls.creator = vtkMRMLLayerDMPipelineScriptedCreator()
        cls.creator.SetPythonCallback(tryCreate)
        vtkMRMLLayerDMPipelineFactory.GetInstance().AddPipelineCreator(cls.creator)

    def LoseFocus(self, eventData: Optional[vtkMRMLInteractionEventData]) -> None:
        super().LoseFocus(eventData)
        self._state = vtkMRMLAbstractWidget.WidgetStateIdle
