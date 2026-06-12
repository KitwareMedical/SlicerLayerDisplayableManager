#include "vtkMRMLNodePythonBridge.h"

// Layer DM includes
#include "vtkMRMLLayerDMPythonUtil.h"

// Slicer includes
#include "vtkMRMLScene.h"

// VTK includes
#include <PyVTKObject.h>
#include <vtkObjectFactory.h>
#include <vtkPythonUtil.h>
#include <vtkSmartPyObject.h>

namespace
{
/// Create a Python wrapper of the given Python type around an existing C++ object.
/// Adapted from VTK's PyVTKObject_FromPointer (Wrapping/PythonCore/PyVTKObject.cxx).
PyObject* CreatePythonNodeWrapper(PyTypeObject* pytype, vtkObjectBase* ptr)
{
  if (!pytype || !ptr)
  {
    return nullptr;
  }

  const std::string classname = ptr->GetClassName();
  PyVTKClass* cls = vtkPythonUtil::FindClass(classname.c_str());
  if (cls == nullptr)
  {
    PyErr_Format(PyExc_ValueError, "internal error, unknown VTK class %.200s", classname.c_str());
    return nullptr;
  }

  // The Python type is a class declared in Python (heap type): keep a reference to it
  // (see PyType_GenericAlloc).
  Py_INCREF(pytype);

  PyObject* pydict = PyDict_New();

  PyVTKObject* self = PyObject_GC_New(PyVTKObject, pytype);

  self->vtk_ptr = ptr;
  self->vtk_flags = 0;
  self->vtk_class = cls;
  self->vtk_dict = pydict;
  self->vtk_buffer = nullptr;
  self->vtk_observers = nullptr;
  self->vtk_weakreflist = nullptr;

  PyObject_GC_Track(self);

  // The Python object owning a VTK object reference is being created.
  // Add the Python object's VTK object reference (this calls ptr->Register).
  vtkPythonUtil::AddObjectToMap(reinterpret_cast<PyObject*>(self), ptr);

  // Call __init__(self) to initialize the Python part of the object and let the
  // bridge bind itself to its Python object (SetPythonObject).
  if (pytype->tp_init != nullptr)
  {
    PyObject* arglist = PyTuple_New(0);
    const int res = pytype->tp_init(reinterpret_cast<PyObject*>(self), arglist, nullptr);
    Py_DECREF(arglist);
    if (res < 0)
    {
      Py_DECREF(self);
      return nullptr;
    }
  }

  return reinterpret_cast<PyObject*>(self);
}
} // namespace

//----------------------------------------------------------------------------
vtkStandardNewMacro(vtkMRMLNodePythonBridge);

//----------------------------------------------------------------------------
vtkMRMLNodePythonBridge::vtkMRMLNodePythonBridge()
  : m_object(nullptr)
{
}

//----------------------------------------------------------------------------
vtkMRMLNodePythonBridge::~vtkMRMLNodePythonBridge()
{
  vtkMRMLLayerDMPythonUtil::DeletePythonObject(&this->m_object);
}

//----------------------------------------------------------------------------
void vtkMRMLNodePythonBridge::SetPythonObject(PyObject* object)
{
  vtkMRMLLayerDMPythonUtil::SetPythonObject(&this->m_object, object);
}

//----------------------------------------------------------------------------
vtkMRMLNode* vtkMRMLNodePythonBridge::CreateNodeInstance()
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return New();
  }

  // Create a new instance using manually wrapped instance using concrete python class
  // Avoid vtkPythonUtil lifetime issues with the newly created VTK instance
  vtkPythonScopeGilEnsurer gilEnsurer;
  PyObject* pyClass = this->CallPythonMethod({}, "GetClass", false);
  if (!pyClass || !PyType_Check(pyClass))
  {
    Py_XDECREF(pyClass);
    return New();
  }

  const auto node = New();
  PyObject* wrapper = CreatePythonNodeWrapper(reinterpret_cast<PyTypeObject*>(pyClass), node);
  Py_DECREF(pyClass);
  Py_XDECREF(wrapper);
  return node;
}

//----------------------------------------------------------------------------
void vtkMRMLNodePythonBridge::ReadXMLAttributes(const char** atts)
{
  this->Superclass::ReadXMLAttributes(atts);

  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  // Convert const char** atts to a Python dictionary
  // atts is a null-terminated list of (key, value) pairs.
  vtkSmartPyObject pyDict(PyDict_New());
  if (atts)
  {
    for (const char** a = atts; *a && *(a + 1); a += 2)
    {
      const char* key = *a;
      const char* value = *(a + 1);
      PyDict_SetItemString(pyDict, key, vtkMRMLLayerDMPythonUtil::ToPyObject(value));
    }
  }

  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs({ static_cast<PyObject*>(pyDict) }), "ReadAttributesFromDict", true);
}

//----------------------------------------------------------------------------
void vtkMRMLNodePythonBridge::WriteXML(ostream& of, int indent)
{
  this->Superclass::WriteXML(of, indent);
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  auto result = this->CallPythonMethod({}, "GetAttributesDict", false);
  if (!result)
  {
    return;
  }
  if (PyDict_Check(result))
  {
    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while (PyDict_Next(result, &pos, &key, &value))
    {
      const char* keyStr = PyUnicode_AsUTF8(key);
      const char* valStr = PyUnicode_AsUTF8(value);
      if (keyStr && valStr)
      {
        of << " " << keyStr << "=\"" << valStr << "\"";
      }
    }
  }
  Py_DECREF(result);
}

//----------------------------------------------------------------------------
void vtkMRMLNodePythonBridge::Copy(vtkMRMLNode* node)
{
  this->Superclass::Copy(node);

  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(node), __func__, true);
}

//----------------------------------------------------------------------------
void vtkMRMLNodePythonBridge::CopyContent(vtkMRMLNode* node, bool deepCopy)
{
  this->Superclass::CopyContent(node, deepCopy);

  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs({ vtkMRMLLayerDMPythonUtil::ToPyObject(node), PyBool_FromLong(deepCopy) }), __func__, true);
}

//----------------------------------------------------------------------------
void vtkMRMLNodePythonBridge::Reset(vtkMRMLNode* defaultNode)
{
  this->Superclass::Reset(defaultNode);

  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(defaultNode), __func__, true);
}

//----------------------------------------------------------------------------
const char* vtkMRMLNodePythonBridge::GetNodeTagName()
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return "MRMLNodePythonBridge";
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  auto result = this->CallPythonMethod({}, __func__, false);
  if (result)
  {
    const char* tagName = PyUnicode_AsUTF8(result);
    m_nodeTagName = tagName ? tagName : "";
    Py_DECREF(result);
    return m_nodeTagName.c_str();
  }
  return "MRMLNodePythonBridge";
}

//----------------------------------------------------------------------------
void vtkMRMLNodePythonBridge::UpdateReferences()
{
  this->Superclass::UpdateReferences();

  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod({}, __func__, true);
}

//----------------------------------------------------------------------------
void vtkMRMLNodePythonBridge::UpdateScene(vtkMRMLScene* scene)
{
  this->Superclass::UpdateScene(scene);

  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod(vtkMRMLLayerDMPythonUtil::ToPyArgs(scene), __func__, true);
}

//----------------------------------------------------------------------------
void vtkMRMLNodePythonBridge::OnNodeAddedToScene()
{
  this->Superclass::OnNodeAddedToScene();

  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return;
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  this->CallPythonMethod({}, __func__, true);
}

//----------------------------------------------------------------------------
vtkObjectBase* vtkMRMLNodePythonBridge::NewInstanceInternal() const
{
  // CreateNodeInstance is in effect const
  return const_cast<vtkMRMLNodePythonBridge*>(this)->CreateNodeInstance();
}

//----------------------------------------------------------------------------
const char* vtkMRMLNodePythonBridge::GetClassNameInternal() const
{
  if (!vtkMRMLLayerDMPythonUtil::IsValidPythonContext())
  {
    return "vtkMRMLNodePythonBridge";
  }

  vtkPythonScopeGilEnsurer gilEnsurer;
  auto result = this->CallPythonMethod({}, "GetClassName", false);
  if (result)
  {
    const char* className = PyUnicode_AsUTF8(result);
    m_className = className ? className : "";
    Py_DECREF(result);
    return m_className.c_str();
  }
  return "vtkMRMLNodePythonBridge";
}

//----------------------------------------------------------------------------
PyObject* vtkMRMLNodePythonBridge::CallPythonMethod(const vtkSmartPyObject& pyArgs, const std::string& fName, bool decrementResult) const
{
  return vtkMRMLLayerDMPythonUtil::CallPythonMethod(this->m_object, pyArgs, fName, decrementResult, this);
}

//----------------------------------------------------------------------------
vtkTypeBool vtkMRMLNodePythonBridge::IsTypeOf(const char* type)
{
  if (!strcmp("vtkMRMLNodePythonBridge", type))
  {
    return 1;
  }
  return Superclass::IsTypeOf(type);
}

//----------------------------------------------------------------------------
vtkTypeBool vtkMRMLNodePythonBridge::IsA(const char* type)
{
  if (!strcmp(this->GetClassName(), type))
  {
    return 1;
  }
  return Superclass::IsA(type);
}

//----------------------------------------------------------------------------
vtkMRMLNodePythonBridge* vtkMRMLNodePythonBridge::SafeDownCast(vtkObjectBase* o)
{
  if (o && o->IsA("vtkMRMLNodePythonBridge"))
  {
    return dynamic_cast<vtkMRMLNodePythonBridge*>(o);
  }
  return nullptr;
}

//----------------------------------------------------------------------------
vtkIdType vtkMRMLNodePythonBridge::GetNumberOfGenerationsFromBaseType(const char* type)
{
  if (!strcmp("vtkMRMLNodePythonBridge", type))
  {
    return 0;
  }
  return 1 + Superclass::GetNumberOfGenerationsFromBaseType(type);
}

//----------------------------------------------------------------------------
vtkIdType vtkMRMLNodePythonBridge::GetNumberOfGenerationsFromBase(const char* type)
{
  return GetNumberOfGenerationsFromBaseType(type);
};

//----------------------------------------------------------------------------
const char* vtkMRMLNodePythonBridge::GetDebugClassName() const
{
  return "vtkMRMLNodePythonBridge";
}
