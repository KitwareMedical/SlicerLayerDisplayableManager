#pragma once

#include "vtkSlicerLayerDMModuleMRMLExport.h"

// Slicer includes
#include "vtkMRMLNode.h"

// VTK includes
#include <vtkPython.h>

class vtkSmartPyObject;

/// \brief C++ Python bridge for the vtkMRMLNode <--> vtkMRMLNodeScripted.
///
/// The class delegates to the Python object implementation for public virtual calls.
/// Only the main virtual methods have been kept from the vtkMRMLNode to avoid cluttering
/// the scripted version.
class VTK_SLICER_LAYERDM_MODULE_MRML_EXPORT vtkMRMLNodePythonBridge : public vtkMRMLNode
{
public:
  static vtkMRMLNodePythonBridge* New();
  using Superclass = vtkMRMLNode;

  void SetPythonObject(PyObject* object);

  vtkMRMLNode* CreateNodeInstance() override;
  void ReadXMLAttributes(const char** atts) override;
  void WriteXML(ostream& of, int indent) override;
  void Copy(vtkMRMLNode* node) override;
  void CopyContent(vtkMRMLNode* node, bool deepCopy) override;
  void Reset(vtkMRMLNode* defaultNode) override;
  const char* GetNodeTagName() override;
  void UpdateReferences() override;
  void UpdateScene(vtkMRMLScene* scene) override;
  void OnNodeAddedToScene() override;

  /// @{
  /// Standard expansion of vtkTypeMacro
  /// Manually expanded to provide GetClassNameInternal and NewInstanceInternal implementations which
  /// will be delegated to Python.
  static vtkTypeBool IsTypeOf(const char* type);
  vtkTypeBool IsA(const char* type) override;
  static vtkMRMLNodePythonBridge* SafeDownCast(vtkObjectBase* o);
  static vtkIdType GetNumberOfGenerationsFromBaseType(const char* type);
  vtkIdType GetNumberOfGenerationsFromBase(const char* type) override;
  /// @}

protected:
  vtkMRMLNodePythonBridge();
  ~vtkMRMLNodePythonBridge() override;

  vtkMRMLNodePythonBridge(const vtkMRMLNodePythonBridge&) = delete;
  void operator=(const vtkMRMLNodePythonBridge&) = delete;

  /// Overridden to let PyObject provide a new node instance if defined.
  vtkObjectBase* NewInstanceInternal() const override;

  /// Overridden to let PyObject provide its class name if defined.
  const char* GetClassNameInternal() const override;

private:
  /// Always return vtkMRMLNodePythonBridge to avoid warnings about removing unknown class.
  const char* GetDebugClassName() const override;
  PyObject* CallPythonMethod(const vtkSmartPyObject& pyArgs, const std::string& fName, bool decrementResult) const;

  PyObject* m_object;
  std::string m_nodeTagName;
  mutable std::string m_className;
};
