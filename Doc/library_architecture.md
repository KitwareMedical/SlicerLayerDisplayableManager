# Library architecture

<div style="text-align: center;">
<img src="https://github.com/KitwareMedical/SlicerLayerDisplayableManager/raw/main/Doc/LayeredDisplayableManager_UML.jpg" width="500"/>
</div>


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
