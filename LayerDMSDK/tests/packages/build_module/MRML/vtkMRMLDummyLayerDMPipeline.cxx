#include "vtkMRMLDummyLayerDMPipeline.h"

#include <vtkObjectFactory.h>

// clang-format completely derp on this files as it doesn't know the macro definitions.
// clang-format off
//---------------------------------------------------------------------------
vtkStandardNewMacro(vtkMRMLDummyLayerDMPipeline)

//---------------------------------------------------------------------------
vtkMRMLDummyLayerDMPipeline::vtkMRMLDummyLayerDMPipeline() {}

//---------------------------------------------------------------------------
vtkMRMLDummyLayerDMPipeline::~vtkMRMLDummyLayerDMPipeline() {}

//---------------------------------------------------------------------------
void vtkMRMLDummyLayerDMPipeline::PrintSelf(ostream& os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os, indent);
  os << indent << "vtkMRMLDummyLayerDMPipeline: " << this->GetClassName() << "\n";
}
// clang-format on
