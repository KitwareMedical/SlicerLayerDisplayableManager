#ifndef vtkMRMLDummyLayerDMPipeline_H_INCLUDED
#define vtkMRMLDummyLayerDMPipeline_H_INCLUDED

#include "vtkDummyMRMLLayerDMPipelineModule.h"

#include <vtkMRMLLayerDMPipeline.h>

class VTK_DUMMY_MRMLLAYERDMPIPELINE_EXPORT vtkMRMLDummyLayerDMPipeline : public vtkMRMLLayerDMPipeline
{
public:
  static vtkMRMLDummyLayerDMPipeline* New();
  vtkTypeMacro(vtkMRMLDummyLayerDMPipeline, vtkMRMLLayerDMPipeline);
  void PrintSelf(ostream& os, vtkIndent indent) override;

protected:
  vtkMRMLDummyLayerDMPipeline();
  ~vtkMRMLDummyLayerDMPipeline() override;
};

#endif
