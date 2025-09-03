# SlicerLayerDisplayableManager

A 3D Slicer module introducing a new displayable manager architecture for layered rendering and interaction handling.

---

## Overview

**SlicerLayerDisplayableManager** is an experimental module designed to simplify the integration of new display
pipelines in 3D Slicer. It introduces a flexible and extensible framework for managing layered rendering, interaction
forwarding, and camera synchronization across multiple pipelines.

This module aims to address common limitations in existing displayable managers by offering a more modular and
injectable design.

---

## Goals

- Factorize pipeline creation and teardown
- Enable layered rendering and interaction forwarding
- Maintain focus continuity across pipelines
- Synchronize cameras across views and layers
- Centralize render request handling

---

## Limitations in Current Displayable Managers

The current displayable manager (DM) architecture in 3D Slicer presents several structural and usability limitations:

- Redundant logic: Each DM reimplements pipeline instantiation and renderer setup independently.
- Custom camera sync: Camera synchronization strategies are manually implemented per DM, leading to inconsistent
  behavior.
- Complexity growth: DMs tend to accumulate unrelated logic over time, making them harder to maintain and extend.
- Focus handling: Focus decisions are based on proximity to interaction only, without consideration for layer priority.
- Factory instantiation: DMs are created using string-based factories, preventing injection of shared dependencies or
  services.

--- 

## Improvements Introduced by SlicerLayerDisplayableManager

The module introduces a new architecture to improve development quality and scalability for visualization widgets:

- Centralized pipeline management: Pipelines are automatically created and deleted by the displayable manager.
- Dependency injection: Lambda and callback-based creators allow find pipeline creation control and injection of shared
  logic at pipeline creation.
- Modular camera synchronization: A dedicated synchronizer handles camera updates across views and layers for pipelines
  following the main camera.
- Layer-aware interaction: Pipelines declare their render layer with arbitrary values, enabling prioritized focus and
  interaction handling without handling the finer grained VTK logic.
- Python integration: A Python abstract class enables rapid development and integration of pipelines.

These changes simplify the development of new widgets, reduce boilerplate, and improve maintainability of existing
visualization components.

---

## Key Features

- Pipeline registration via factory and creator API
- Lambda and callback support for dependency injection
- Customizable observer update pattern
- First-class Python abstract pipeline class

> WARNING : **Experimental Module**  
> API may change or break between versions. Under review by the 3D Slicer community for potential core integration.

---

## Core Classes

| Class                                 | Description                                                                                  |
|---------------------------------------|----------------------------------------------------------------------------------------------|
| vtkMRMLLayerDMPipelineI               | Interface for display pipelines. Handles interaction, rendering, camera, and observer logic. |
| vtkMRMLLayerDisplayableManager        | Main displayable manager. Initializes pipeline manager and delegates scene updates.          |
| vtkMRMLLayerDMCameraSynchronizer      | Synchronizes default camera with renderer or slice node state.                               |
| vtkMRMLLayerDMLayerManager            | Manages renderer layers based on pipeline layer/camera pairs.                                |
| vtkMRMLLayerDMPipelineCreatorI        | Interface for pipeline creation. Supports custom instantiation logic.                        |
| vtkMRMLLayerDMPipelineCallbackCreator | Callback-based implementation of pipeline creator.                                           |
| vtkMRMLLayerDMPipelineScriptedCreator | Python lambda-based pipeline creator.                                                        |
| vtkMRMLLayerDMPipelineFactory         | Singleton factory for pipeline instantiation and registration.                               |
| vtkMRMLLayerDMPipelineManager         | Manages pipeline lifecycle, layer manager, and camera sync.                                  |
| vtkMRMLLayerDMScriptedPipelineBridge  | Python bridge for virtual method delegation.                                                 |
| vtkMRMLLayerDMScriptedPipeline        | Python abstract class for scripted pipelines.                                                |

---

## Architecture diagram :

<img src="https://github.com/Thibault-Pelletier/SlicerLayerDisplayableManager/raw/main/Doc/LayeredDisplayableManager_UML.jpg" width="500"/>

---

## API from `vtkMRMLLayerDMPipelineI`

<img src="https://github.com/Thibault-Pelletier/SlicerLayerDisplayableManager/raw/main/Doc/PipelineI_API.jpg" width="500"/>

```cpp
New() -> vtkMRMLLayerDMPipelineI*
CanProcessInteractionEvent(vtkMRMLInteractionEventData* eventData, double& distance2) -> bool
GetCamera() const -> vtkCamera*
GetMouseCursor() const -> int
GetRenderLayer() const -> unsigned int
GetWidgetState() const -> int
LoseFocus(vtkMRMLInteractionEventData* eventData) -> void
OnDefaultCameraModified(vtkCamera* camera) -> void
OnRendererAdded(vtkRenderer* renderer) -> void
OnRendererRemoved(vtkRenderer* renderer) -> void
ProcessInteractionEvent(vtkMRMLInteractionEventData* eventData) -> bool
SetDisplayNode(vtkMRMLNode* displayNode) -> void
SetPipelineManager(vtkMRMLLayerDMPipelineManager* pipelineManager) -> void
SetScene(vtkMRMLScene* scene) -> void
SetViewNode(vtkMRMLAbstractViewNode* viewNode) -> void
UpdatePipeline() -> void
BlockResetDisplay(bool isBlocked) -> bool
GetDisplayNode() const -> vtkMRMLNode*
GetNodePipeline(vtkMRMLNode* node) const -> vtkMRMLLayerDMPipelineI*
GetRenderer() const -> vtkRenderer*
GetScene() const -> vtkMRMLScene*
GetViewNode() const -> vtkMRMLAbstractViewNode*
UpdateObserver(vtkObject* prevObj, vtkObject* obj, const std::vector<unsigned long>& events) const -> bool
UpdateObserver(vtkObject* prevObj, vtkObject* obj, unsigned long event) const -> bool
ResetDisplay() -> void
RequestRender() const -> void
SetRenderer(vtkRenderer* renderer) -> void
vtkMRMLLayerDMPipelineI()
~vtkMRMLLayerDMPipelineI()
OnUpdate(vtkObject* obj, unsigned long eventId, void* callData) -> void
```

---

## Python Integration

- Python pipelines can be created using
  `from LayerDMManagerLib.vtkMRMLLayerDMScriptedPipeline import vtkMRMLLayerDMScriptedPipeline`
- Scripted creators allow dynamic injection of pipeline logic
- Ideal for prototyping and rapid development

---

## Status

This module is under active development and experimentation. Contributions and feedback from the 3D Slicer community are
welcome to refine its design and promote future integration into the core.

---

## Getting Started

To use this module:

1. Register your pipeline using the factory API
2. Implement your pipeline logic via `vtkMRMLLayerDMPipelineI` or its Python counterpart
3. Inject your creator using callback or scripted creator
4. Let the displayable manager handle the rest
