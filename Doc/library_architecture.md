# Library architecture

## Layer DM classes

The LayerDisplayableManager is the main entry point for the classes in this extension.
It's automatically registered in the default 3D Slicer SliceViews and ThreeDViews as a normal displayable manager when
the module is first setup using conventional 3D Slicer mechanisms.

Internally, the Layer displayable manager delegates to the following objects.

* pipeline manager: used for the lifetime of the created pipelines.
* layer manager: used for the creation / deletion of the renderers added to the render window and managed by the layer
* camera synchronizer: used for camera synchronization and callback mechanism linked to the default view camera.

```{tip}
From a user standpoint, only the following classes need to be manipulated directly:

* The pipeline: either implemented in Python or in C++
* The pipeline creator: Responsible for creating the pipeline through a user set callback
* The pipeline factory: Accessible through a singleton and used automatically by the displayable manager
```

The diagram below summarizes the relationship between the different classes.

```{eval-rst}
.. mermaid:: diagrams/layer_dm_collaboration.mmd
   :align: center
```

The main classes of the library and their responsibilities are summarized below :

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

## Pipeline lifecycle

The sequence diagram below shows a typical pipeline lifecycle as handled by the library:

```{eval-rst}
.. mermaid:: diagrams/layer_dm_pipeline_lifecycle_sequence.mmd
   :align: center
```

## Interaction handling

The diagram below shows how the LayerDM handles interactions :

```{eval-rst}
.. mermaid:: diagrams/layer_dm_interaction_sequence.mmd
   :align: center
```

During interactions, the cap process / process and lose focus events are forwarded to the interaction logic class
responsible for handling the events.

The interaction logic will forward the events to the underlying pipelines.

Pipelines that can process the interaction will be sorted using a tuple of three values:

* Pipeline widget state: if its value is greater than hovered indicating and active user interaction with the pipeline
* Pipeline render order: greater values indicate that pipelines are rendered over other pipelines
* Pipeline distance to interaction

This strategy provides intuitive interactions for users depending on the type of widgets they are manipulating.
