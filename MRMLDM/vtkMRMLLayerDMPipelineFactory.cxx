#include "vtkMRMLLayerDMPipelineFactory.h"

// Layer DM includes
#include "vtkMRMLLayerDMPipelineCreatorI.h"
#include "vtkMRMLLayerDMPipelineCallbackCreator.h"
#include "vtkMRMLLayerDMPipelineI.h"

// VTK includes
#include <vtkCommand.h>
#include <vtkObjectFactory.h>

vtkStandardNewMacro(vtkMRMLLayerDMPipelineFactory);

vtkSmartPointer<vtkMRMLLayerDMPipelineFactory> vtkMRMLLayerDMPipelineFactory::GetInstance()
{
  static vtkSmartPointer<vtkMRMLLayerDMPipelineFactory> instance = vtkSmartPointer<vtkMRMLLayerDMPipelineFactory>::New();
  return instance;
}

void vtkMRMLLayerDMPipelineFactory::AddPipelineCreator(const vtkSmartPointer<vtkMRMLLayerDMPipelineCreatorI>& creator)
{
  if (this->ContainsPipelineCreator(creator))
  {
    return;
  }

  this->m_pipelineCreators.emplace_back(creator);
  this->InvokeEvent(vtkCommand::ModifiedEvent);
}

vtkSmartPointer<vtkMRMLLayerDMPipelineCreatorI> vtkMRMLLayerDMPipelineFactory::AddPipelineCreator(
  const std::function<vtkSmartPointer<vtkMRMLLayerDMPipelineI>(vtkMRMLAbstractViewNode*, vtkMRMLNode*)>& creatorCallBack)
{
  auto creator = vtkSmartPointer<vtkMRMLLayerDMPipelineCallbackCreator>::New();
  creator->SetCallback(creatorCallBack);
  this->AddPipelineCreator(creator);
  return creator;
}

void vtkMRMLLayerDMPipelineFactory::RemovePipelineCreator(const vtkSmartPointer<vtkMRMLLayerDMPipelineCreatorI>& creator)
{
  size_t prevSize = this->m_pipelineCreators.size();
  this->m_pipelineCreators.erase(std::remove_if(this->m_pipelineCreators.begin(),
                                                this->m_pipelineCreators.end(),
                                                [creator](const vtkSmartPointer<vtkMRMLLayerDMPipelineCreatorI>& value) { return value == creator; }),
                                 this->m_pipelineCreators.end());
  if (this->m_pipelineCreators.size() != prevSize)
  {
    this->InvokeEvent(vtkCommand::ModifiedEvent);
  }
}

bool vtkMRMLLayerDMPipelineFactory::ContainsPipelineCreator(const vtkSmartPointer<vtkMRMLLayerDMPipelineCreatorI>& creator) const
{
  return std::find(this->m_pipelineCreators.begin(), this->m_pipelineCreators.end(), creator) != this->m_pipelineCreators.end();
}

vtkSmartPointer<vtkMRMLLayerDMPipelineI> vtkMRMLLayerDMPipelineFactory::CreatePipeline(vtkMRMLAbstractViewNode* viewNode, vtkMRMLNode* node)
{
  for (const auto& ctor : m_pipelineCreators)
  {
    if (auto created = ctor->CreatePipeline(viewNode, node))
    {
      this->m_lastView = viewNode;
      this->m_lastNode = node;
      this->m_lastPipeline = created;
      this->InvokeEvent(PipelineAboutToBeCreatedEvent);
      return created;
    }
  }

  return {};
}

vtkMRMLAbstractViewNode* vtkMRMLLayerDMPipelineFactory::GetLastViewNode() const
{
  return this->m_lastView;
}

vtkMRMLNode* vtkMRMLLayerDMPipelineFactory::GetLastNode() const
{
  {
    return this->m_lastNode;
  }
}

vtkMRMLLayerDMPipelineI* vtkMRMLLayerDMPipelineFactory::GetLastPipeline() const
{
  {
    return this->m_lastPipeline;
  }
}

vtkMRMLLayerDMPipelineFactory::vtkMRMLLayerDMPipelineFactory()
  : m_lastView(nullptr)
  , m_lastNode(nullptr)
  , m_lastPipeline(nullptr)
{
}