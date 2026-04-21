import slicer
from slicer.ScriptedLoadableModule import ScriptedLoadableModule, ScriptedLoadableModuleWidget


class PrintModelName(ScriptedLoadableModule):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.title = "PrintModelName LayerDM"
        self.parent.categories = ["Examples"]
        self.parent.dependencies = []
        self.parent.contributors = []
        self.parent.helpText = ""
        self.parent.acknowledgementText = ""


class PrintModelNameWidget(ScriptedLoadableModuleWidget):
    def setup(self):
        import qt

        super().setup()

        createSphereButton = qt.QPushButton("Create sphere")
        createSphereButton.clicked.connect(self._onCreateSphereClicked)
        self.layout.addWidget(createSphereButton)
        self.layout.addStretch()

    def _onCreateSphereClicked(self):
        from PrintModelNameLib import PrintModelNameDMPipeline
        from vtk import vtkSphereSource
        import random

        PrintModelNameDMPipeline.RegisterPipeline()
        sphereSource = vtkSphereSource()
        sphereSource.SetCenter(random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10))
        sphereSource.SetRadius(random.uniform(0.1, 1.0))
        sphereSource.Update()

        modelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode")
        modelNode.SetAndObservePolyData(sphereSource.GetOutput())
        modelNode.CreateDefaultDisplayNodes()
        PrintModelNameDMPipeline.CreatePipelineNode(modelNode)

    def onReload(self):
        import importlib.util
        import sys

        package_name = "PrintModelNameLib"
        submodule_names = ["print_model_name_dm_pipeline"]

        # Load the main package
        print(f"Loading package {package_name}")
        importlib.import_module(package_name)

        # Reload submodules
        for submodule_name in submodule_names:
            full_name = f"{package_name}.{submodule_name}"
            print(f"Reloading {full_name}")

            if full_name in sys.modules:
                module = sys.modules[full_name]
                importlib.reload(module)
            else:
                importlib.import_module(full_name)

        ScriptedLoadableModuleWidget.onReload(self)
