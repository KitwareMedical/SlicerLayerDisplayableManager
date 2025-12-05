#pragma once

#include "vtkSlicerModelGlowModuleMRMLExport.h"

// Slicer includes
#include "vtkMRMLLayerDMPipelineI.h"

// VTK includes
#include <vtkSmartPointer.h>
#include <vtkWeakPointer.h>

class vtkMRMLModelNode;
class vtkMRMLInteractionEventData;

class vtkActor;
class vtkRenderer;

class VTK_SLICER_MODEL_GLOW_MODULE_MRML_EXPORT vtkMRMLModelGlowPipeline : public vtkMRMLLayerDMPipelineI
{
public:
  static vtkMRMLModelGlowPipeline* New();
  vtkTypeMacro(vtkMRMLModelGlowPipeline, vtkMRMLLayerDMPipelineI);

  void SetDisplayNode(vtkMRMLNode* displayNode) override;
  void OnRendererRemoved(vtkRenderer* renderer) override;
  void OnRendererAdded(vtkRenderer* renderer) override;
  unsigned int GetRenderOrder() const override;
  void UpdatePipeline() override;
  // void SetViewNode(vtkMRMLAbstractViewNode* viewNode) override;
  // void SetScene(vtkMRMLScene* scene) override;

  bool CanProcessInteractionEvent(vtkMRMLInteractionEventData* eventData, double& distance2) override;
  bool ProcessInteractionEvent(vtkMRMLInteractionEventData* eventData) override;
  void LoseFocus(vtkMRMLInteractionEventData* eventData) override;
  // int GetMouseCursor() const override;
  // void OnDefaultCameraModified(vtkCamera* camera) override;
  // int GetWidgetState() const override;

protected:
  vtkMRMLModelGlowPipeline();
  ~vtkMRMLModelGlowPipeline() override;
  vtkMRMLModelGlowPipeline(const vtkMRMLModelGlowPipeline&) = delete;
  void operator=(const vtkMRMLModelGlowPipeline&) = delete;

private:
  void OnUpdate(vtkObject* node, unsigned long eventId, void* callData) override;
  void SetModelNode(vtkMRMLModelNode* node);

  vtkWeakPointer<vtkMRMLModelNode> ModelNode{ nullptr };
  vtkNew<vtkActor> GlowActor;
};
