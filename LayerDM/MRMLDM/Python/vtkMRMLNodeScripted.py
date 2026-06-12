import base64
import json
import slicer
from slicer import vtkMRMLNodePythonBridge, vtkMRMLScene, vtkMRMLNode
from types import UnionType
from typing import get_args, get_origin, Union


class NodeProperty:
    """
    Descriptor pattern for properties attached to a vtkMRMLNodeScripted instance.
    Allows to Serialize / Deserialize / Trigger Modify for the underlying node.
    """

    def __init__(self, default=None, default_factory=None, do_serialize: bool = True, encoder=None, decoder=None):
        self._default = default
        self._default_factory = default_factory
        self._do_serialize = do_serialize
        self._encoder = encoder
        self._decoder = decoder

    def __set_name__(self, owner, name):
        if not issubclass(owner, vtkMRMLNodeScripted):
            _error_msg = f"Invalid input type {owner}. Expected an instance of vtkMRMLNodeScripted."
            raise TypeError(_error_msg)

        self._name = name
        self._private_name = f"__{name}"
        self._type_hints = owner.__annotations__.get(name, None)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        assert isinstance(instance, vtkMRMLNode)
        try:
            return getattr(instance, self._private_name)
        except AttributeError:
            return None

    def __set__(self, instance: vtkMRMLNode, value):
        if instance is None:
            return

        current_value = self.__get__(instance, type(instance))
        if current_value == value:
            return
        setattr(instance, self._private_name, value)
        instance.Modified()

    def to_string(self, instance) -> str:
        value = self.__get__(instance, type(instance))
        raw = json.dumps(value, default=self._encoder)
        return base64.b64encode(raw.encode("utf-8")).decode("ascii")

    def from_string(self, instance, value: str) -> None:
        raw = base64.b64decode(value.encode("ascii"))
        value = json.loads(raw.decode("utf-8"), object_hook=self._decoder)
        self.__set__(instance, value)

    def reset(self, instance) -> None:
        default_value = self._default
        if default_value is None and callable(self._default_factory):
            default_value = self._default_factory()
        elif self.is_optional:
            default_value = None
        else:
            default_value = self._get_type_hint_default(self._type_hints)
        self.__set__(instance, default_value)

    @property
    def name(self):
        return self._name

    @property
    def is_optional(self) -> bool:
        if self._type_hints is None:
            return True

        if self._is_union_type(self._type_hints):
            return any(type_hint is type(None) for type_hint in get_args(self._type_hints))

        return self._type_hints is type(None)

    @property
    def do_serialize(self) -> bool:
        return self._do_serialize

    @classmethod
    def _is_union_type(cls, type_hint):
        return get_origin(type_hint) is Union or isinstance(type_hint, UnionType)

    @classmethod
    def _get_type_hint_default(cls, type_hint):
        if cls._is_union_type(type_hint):
            return any(cls._get_type_hint_default(sub_hint) for sub_hint in get_args(type_hint)) or None
        if callable(type_hint):
            return type_hint()
        return None


class vtkMRMLNodeScripted(vtkMRMLNodePythonBridge):
    """
    Python base class for scripted MRML nodes.
    Can be registered in the scene using the RegisterInScene class method.

    Relies on JSON encoding / decoding for encoding NodeProperty on scene save.
    To serialize new types,
    """

    def __init__(self):
        self.SetPythonObject(self)

        for node_prop in node_properties(self):
            node_prop.reset(self)

    def CreateNodeInstance(self) -> vtkMRMLNode:
        """
        Create a new instance of the node.
        """
        return type(self)()

    def ReadAttributesFromDict(self, atts: dict[str, str]) -> None:
        """
        Read node attributes from the dictionary.
        """

        for node_prop in node_properties(self):
            if not node_prop.do_serialize:
                continue

            value = atts.get(node_prop.name)
            if isinstance(value, str):
                node_prop.from_string(self, value)
            else:
                node_prop.reset(self)

            if value is None and not node_prop.is_optional:
                continue

    def GetAttributesDict(self) -> dict[str, str] | None:
        """
        Returns the node attributes as dictionary.
        """
        return {
            node_prop.name: node_prop.to_string(self) for node_prop in node_properties(self) if node_prop.do_serialize
        }

    def Copy(self, node: vtkMRMLNode) -> None:
        """
        Copy the node's state.
        """
        pass

    def CopyContent(self, node: vtkMRMLNode, deepCopy: bool) -> None:
        """
        Copy the node's content.
        """
        pass

    def Reset(self, defaultNode: vtkMRMLNode) -> None:
        """
        Reset the node to its default state.
        """
        pass

    def GetClass(self):
        return type(self)

    def GetClassName(self):
        """
        Get the name of the class. Used in Scene registration.
        """
        return self.GetClass().__name__

    def GetNodeTagName(self) -> str:
        """
        Get the XML tag name for the node.
        """
        return self.GetClassName()

    def UpdateReferences(self) -> None:
        """
        Update node references.
        """
        pass

    def UpdateScene(self, scene: vtkMRMLScene) -> None:
        """
        Update the node after being added to a scene.
        """
        pass

    def OnNodeAddedToScene(self) -> None:
        """
        Callback for when the node is added to a scene.
        """
        pass

    @classmethod
    def RegisterInScene(cls, scene: vtkMRMLScene | None = None) -> None:
        if scene is None:
            scene = slicer.mrmlScene

        node = cls()
        if not scene.IsNodeClassRegistered(node.GetClassName()):
            scene.RegisterNodeClass(node)


def node_properties(node: vtkMRMLNodeScripted | None) -> list[NodeProperty]:
    """
    Returns the list of node properties attached to the input mrml node instance.
    If the node doesn't contain any property, or is None, returns an empty list.
    """

    if not isinstance(node, vtkMRMLNodeScripted):
        return []

    node_type = type(node)
    return [
        getattr(node_type, attr_name)
        for attr_name in dir(node_type)
        if isinstance(getattr(node_type, attr_name), NodeProperty)
    ]
