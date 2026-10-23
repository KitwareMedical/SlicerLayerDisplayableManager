"""
Helpers used by the LayerDM tests so that they can run both:
  - inside the 3D Slicer application (extension testing),
  - in a plain Python / Pytest / VTK / slicer-core environment (wheel testing).

The tests build their own MRML scene with :func:`create_test_scene` instead of
using the ``slicer.mrmlScene`` singleton, which is only set inside the 3D Slicer
application. The ``ScriptedLoadableModuleTest`` helper class provided by 3D
Slicer is also only available there, so this module falls back to
``unittest.TestCase`` when it cannot be imported.
"""

import subprocess
import sys
import textwrap
import unittest

try:
    # Only available when running inside the 3D Slicer application
    from slicer.ScriptedLoadableModule import ScriptedLoadableModuleTest
except ImportError:
    # unittest.TestCase is used instead so that the tests can be collected and
    # run by pytest (which honors setUp/tearDown) outside of 3D Slicer.
    ScriptedLoadableModuleTest = unittest.TestCase


def create_test_scene():
    """
    Create the MRML scene used by a test.

    On top of a plain ``vtkMRMLScene``, this:
      - creates the interaction and selection singleton nodes,
      - registers the LayerDM MRML nodes in the scene (which is done by the
        module logic at application startup in 3D Slicer).

    The MRML node classes are registered in the scene itself, so each test needs
    its own scene. The scene also keeps the logic instances it depends on alive.
    """
    from slicer import vtkMRMLApplicationLogic, vtkMRMLScene, vtkSlicerLayerDMLogic

    scene = vtkMRMLScene()

    # Creates the interaction & selection singleton nodes
    applicationLogic = vtkMRMLApplicationLogic()
    applicationLogic.SetMRMLScene(scene)

    # Registers the LayerDM MRML nodes in the scene
    moduleLogic = vtkSlicerLayerDMLogic()
    moduleLogic.SetMRMLScene(scene)
    moduleLogic.RegisterNodes()

    # Keep the logic instances alive for as long as the scene is used
    scene.applicationLogic = applicationLogic
    scene.moduleLogic = moduleLogic
    return scene


def save_scene(scene, path) -> None:
    """
    Save the input scene to the input ``.mrml`` or ``.mrb`` path.

    The scene is written directly instead of going through
    ``slicer.util.saveScene``, which only saves the 3D Slicer application scene.
    """
    scene.SetURL(str(path))
    scene.Commit()


def load_scene(scene, path) -> None:
    """
    Load the input ``.mrml`` or ``.mrb`` path into the input scene.

    The scene is read directly instead of going through ``slicer.util.loadScene``,
    which only loads into the 3D Slicer application scene.
    """
    scene.SetURL(str(path))
    scene.Connect()


def create_render_window(size=(300, 300)):
    """
    Create a render window which can be used to drive displayable managers.

    Return a ``(vtkRenderWindow, vtkRenderer)`` tuple.

    Note: the render window needs an interactor. Otherwise, instantiating the
    displayable managers of a ``vtkMRMLDisplayableManagerGroup`` would crash.
    """
    from vtk import vtkInteractorStyle, vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor

    renderWindow = vtkRenderWindow()
    # Offscreen rendering avoids popping up windows when running the tests
    renderWindow.SetOffScreenRendering(True)
    renderer = vtkRenderer()
    renderWindow.AddRenderer(renderer)

    interactor = vtkRenderWindowInteractor()
    interactor.SetInteractorStyle(vtkInteractorStyle())
    renderWindow.SetInteractor(interactor)

    renderWindow.SetSize(int(size[0]), int(size[1]))
    return renderWindow, renderer


_RENDER_PROBE_SCRIPT = """
import vtk

renderWindow = vtk.vtkRenderWindow()
renderWindow.SetOffScreenRendering(True)
renderer = vtk.vtkRenderer()
renderWindow.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(vtk.vtkInteractorStyle())
renderWindow.SetInteractor(interactor)
renderWindow.SetSize(64, 64)
renderWindow.Render()
"""

_renderingSupported = None


def is_rendering_supported():
    global _renderingSupported
    if _renderingSupported is None:
        _renderingSupported = _probe_rendering()
    return _renderingSupported


def _probe_rendering(timeout=120):
    command = [sys.executable, "-c", textwrap.dedent(_RENDER_PROBE_SCRIPT)]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
    except (OSError, subprocess.SubprocessError):
        return False
    return completed.returncode == 0
