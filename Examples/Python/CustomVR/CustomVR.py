"""
This example shows how to create a custom volume rendering for a volume node using the SlicerLayerDisplayableManager
extension.

It goes over the following concepts:
    - Creates a VR display pipeline on a selected volume node in the scene
    - Register the pipeline creation mechanism

Usage:
    This example is implemented as a scripted module and can be added as such to Slicer.
    Due to import order considerations, the pipeline code is lazy loaded from the CustomVRLib python package.
"""

import qt
import slicer
from slicer.ScriptedLoadableModule import ScriptedLoadableModule, ScriptedLoadableModuleWidget


class CustomVR(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Custom VR Pipeline Example"
        self.parent.categories = ["qSlicerAbstractCoreModule", "Examples"]
        self.parent.dependencies = []
        self.parent.contributors = []
        self.parent.helpText = ""
        self.parent.acknowledgementText = ""


class CustomVRWidget(ScriptedLoadableModuleWidget):
    """
    In this example, we will display a custom volume rendering and use VTK compute shader for processing the volume.
    To avoid initialization problems, the pipeline registration is done lazily during the setup.
    """

    def setup(self) -> None:
        from CustomVRLib import registerPipeline

        registerPipeline()
        ScriptedLoadableModuleWidget.setup(self)

        widget = qt.QWidget()
        layout = qt.QVBoxLayout(widget)

        # Configure volume selector node
        self._volumeNodeSelector = slicer.qMRMLNodeComboBox(widget)
        self._volumeNodeSelector.nodeTypes = ["vtkMRMLVolumeNode"]
        self._volumeNodeSelector.selectNodeUponCreation = True
        self._volumeNodeSelector.addEnabled = False
        self._volumeNodeSelector.removeEnabled = False
        self._volumeNodeSelector.showHidden = False
        self._volumeNodeSelector.renameEnabled = True
        self._volumeNodeSelector.setMRMLScene(slicer.mrmlScene)
        layout.addWidget(self._volumeNodeSelector)

        # Configure toggle button
        toggleDisplayButton = qt.QPushButton("Toggle display")
        toggleDisplayButton.clicked.connect(self._toggleVolumeDisplay)
        layout.addWidget(toggleDisplayButton)
        layout.addStretch()

        self.layout.addWidget(widget)

    def _toggleVolumeDisplay(self, *_):
        from CustomVRLib import CustomVRPipeline

        volumeNode = self._volumeNodeSelector.currentNode()
        if not volumeNode:
            return

        wasVisible = CustomVRPipeline.GetVRNodeVisibility(volumeNode, slicer.mrmlScene)
        vrNode = CustomVRPipeline.CreateVRNode(volumeNode, slicer.mrmlScene)
        CustomVRPipeline.SetVRNodeVisible(vrNode, not wasVisible)

    def onReload(self):
        """
        Customization of reload to allow reloading of the CustomVRLib files.
        """
        import importlib

        packageName = "CustomVRLib"
        submodules = ["CustomVRPipeline"]

        # Reload the package
        module = importlib.import_module(packageName)
        importlib.reload(module)

        # Reload submodules
        for sub in submodules:
            fullName = f"{packageName}.{sub}"
            submodule = importlib.import_module(fullName)
            importlib.reload(submodule)

        ScriptedLoadableModuleWidget.onReload(self)
