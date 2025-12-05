# Introduction

Although 3D Slicer provides an architecture to customize its view widgets and rendering, implementing new widgets is a
significant challenge.

To properly function a significant number of elements need to be created / assembled / manipulated :

* A MRML Node to store the display information and trigger the creation of the VTK pipelines from the scene
* A Displayable Manager responsible for creating a VTK pipeline based on the type of view / information present in the
  MRML node.
* A VTK render window to add new renderers if our widget needs to be displayed in overlay
* The actual VTK widget / representation for handling the user events
* ...


Implementing and connecting all these elements have restricted the implementation of new displayable managers to 3D
Slicer expert developers.

For new developers, it was mainly recommended for interactive behaviors to:
* Compose existing nodes in Python and [use markups points for interactivity](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html#specify-a-sphere-by-multiple-control-points)
* Fetch access to the render window from the Qt widgets and [directly inject their actors](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html#access-vtk-rendering-classes)


The LayerDM library was created to ease the creation of new VTK pipelines by:
* Automating a lot of boilerplate
  * Pipeline creation/removal mechanism based on scene nodes
  * Camera synchronization
  * Renderer layer creation / removal
  * Rendering reactivity based on object's event

* Providing a simple API
  * Explicit pipeline creation callbacks
  * Python bridges and wrapping
  * Improved event processing order
  * Access to sibling pipelines


```{note}
The library doesn't replace the current displayable manager system but is integrated into it making it fully compatible
with existing displayable managers and event processing mechanism.
```

## Installing the extension

The library can be installed through the
[extension manager](https://slicer.readthedocs.io/en/latest/user_guide/extensions.html#extensions).

Once the library is installed, you can checkout the [examples](examples.md) to get started developing your own
pipelines.
