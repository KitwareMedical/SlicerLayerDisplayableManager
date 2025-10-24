#include "vtkMRMLLayerDMScriptedPipelineBridge.h"

// Layer DM includes
#include "vtkMRMLLayerDMPipelineManager.h"

// Slicer includes
#include "vtkMRMLInteractionEventData.h"
#include "vtkMRMLLayerDMPythonUtil.h"
#include "vtkMRMLScene.h"

// VTK includes
#include <object.h>
#include <vtkCamera.h>
#include <vtkObject.h>
#include <vtkObjectFactory.h>
#include <vtkPythonUtil.h>
#include <vtkRenderer.h>

vtkStandardNewMacro(vtkMRMLLayerDMScriptedPipelineBridge);

void vtkMRMLLayerDMScriptedPipelineBridge::UpdatePipeline()
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  this->CallPythonMethod({}, __func__);
}

PyObject* vtkMRMLLayerDMScriptedPipelineBridge::CastCallData(PyObject* object, int vtkType)
{
  return vtkMRMLLayerDMPythonUtil::CastCallData(object, vtkType);
}

vtkMRMLLayerDMScriptedPipelineBridge::vtkMRMLLayerDMScriptedPipelineBridge()
  : m_object{ nullptr }
{
}

vtkMRMLLayerDMScriptedPipelineBridge::~vtkMRMLLayerDMScriptedPipelineBridge()
{
  vtkMRMLLayerDMPythonUtil::DeletePythonObject(&this->m_object);
}

bool vtkMRMLLayerDMScriptedPipelineBridge::CanProcessInteractionEvent(vtkMRMLInteractionEventData* eventData, double& distance2)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return false;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  if (auto result = this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(eventData), __func__))
  {
    int canProcess;
    if (PyTuple_Check(result) && PyArg_ParseTuple(result, "pd", &canProcess, &distance2))
    {
      return canProcess;
    }

    // Unpack error or unexpected return type
    PyErr_SetString(PyExc_TypeError, "Expected a tuple[bool, float] return type");
  }

  return false;
}

vtkCamera* vtkMRMLLayerDMScriptedPipelineBridge::GetCamera() const
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return Superclass::GetCamera();
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  auto result = this->CallPythonMethod({}, __func__);
  if (result && (result != Py_None))
  {
    return vtkCamera::SafeDownCast(vtkPythonUtil::GetPointerFromObject(result, "vtkCamera"));
  }
  return Superclass::GetCamera();
}

int vtkMRMLLayerDMScriptedPipelineBridge::GetMouseCursor() const
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return Superclass::GetMouseCursor();
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  if (auto result = this->CallPythonMethod({}, __func__))
  {
    return PyLong_AsLong(result);
  }
  return Superclass::GetMouseCursor();
}

unsigned int vtkMRMLLayerDMScriptedPipelineBridge::GetRenderOrder() const
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return Superclass::GetRenderOrder();
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  if (auto result = this->CallPythonMethod({}, __func__))
  {
    return PyLong_AsLong(result);
  }
  return Superclass::GetRenderOrder();
}

int vtkMRMLLayerDMScriptedPipelineBridge::GetWidgetState() const
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return Superclass::GetWidgetState();
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  if (auto result = this->CallPythonMethod({}, __func__))
  {
    return PyLong_AsLong(result);
  }
  return Superclass::GetWidgetState();
}

void vtkMRMLLayerDMScriptedPipelineBridge::LoseFocus(vtkMRMLInteractionEventData* eventData)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(eventData), __func__);
}

void vtkMRMLLayerDMScriptedPipelineBridge::OnDefaultCameraModified(vtkCamera* camera)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(camera), __func__);
}

void vtkMRMLLayerDMScriptedPipelineBridge::OnRendererAdded(vtkRenderer* renderer)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(renderer), __func__);
}

void vtkMRMLLayerDMScriptedPipelineBridge::OnRendererRemoved(vtkRenderer* renderer)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(renderer), __func__);
}

bool vtkMRMLLayerDMScriptedPipelineBridge::ProcessInteractionEvent(vtkMRMLInteractionEventData* eventData)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return false;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  if (auto result = this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(eventData), __func__))
  {
    return result == Py_True;
  }
  return false;
}

void vtkMRMLLayerDMScriptedPipelineBridge::SetDisplayNode(vtkMRMLNode* displayNode)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(displayNode), __func__);
}

void vtkMRMLLayerDMScriptedPipelineBridge::SetViewNode(vtkMRMLAbstractViewNode* viewNode)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(viewNode), __func__);
}

void vtkMRMLLayerDMScriptedPipelineBridge::SetScene(vtkMRMLScene* scene)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(scene), __func__);
}

void vtkMRMLLayerDMScriptedPipelineBridge::SetPipelineManager(vtkMRMLLayerDMPipelineManager* pipelineManager)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(pipelineManager), __func__);
}

void vtkMRMLLayerDMScriptedPipelineBridge::SetPythonObject(PyObject* object)
{
  vtkMRMLLayerDMPythonUtil::SetPythonObject(&this->m_object, object);
}

void vtkMRMLLayerDMScriptedPipelineBridge::OnUpdate(vtkObject* obj, unsigned long eventId, void* callData)
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  auto result = this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(obj, eventId, callData), __func__);
  vtkMRMLLayerDMPythonUtil::DecrementResultAndErrorMacroOnPyError(result, "vtkMRMLLayerDMScriptedPipelineBridge::OnUpdate");
}

PyObject* vtkMRMLLayerDMScriptedPipelineBridge::CallPythonMethod(const vtkSmartPyObject& pyArgs, const std::string& fName) const
{
  return vtkMRMLLayerDMPythonUtil::CallPythonMethod(this->m_object, pyArgs, fName);
}
