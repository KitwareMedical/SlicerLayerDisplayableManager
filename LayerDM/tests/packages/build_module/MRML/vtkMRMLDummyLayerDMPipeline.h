#ifndef vtkMRMLDummyLayerDMPipeline_H_INCLUDED
#define vtkMRMLDummyLayerDMPipeline_H_INCLUDED

#include "vtkDummyMRMLLayerDMPipelineModule.h"

#include <vtkMRMLLayerDMPipelineI.h>

class VTK_DUMMY_MRMLLAYERDMPIPELINE_EXPORT vtkMRMLDummyLayerDMPipeline : public vtkMRMLLayerDMPipelineI
{
public:
  static vtkMRMLDummyLayerDMPipeline* New();
  vtkTypeMacro(vtkMRMLDummyLayerDMPipeline, vtkMRMLLayerDMPipelineI);
  void PrintSelf(ostream& os, vtkIndent indent) override;

protected:
  vtkMRMLDummyLayerDMPipeline();
  ~vtkMRMLDummyLayerDMPipeline() override;
};

#endif
