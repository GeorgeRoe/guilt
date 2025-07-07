from typing import Type, Any, TypeVar, cast
import inspect
from dataclasses import is_dataclass

T = TypeVar("T")

class DependencyInjector:
  def __init__(self) -> None:
    self._bindings: dict[Type[Any], Type[Any]] = {}
    self._instances: dict[Type[Any], Any] = {}
    
  def bind(self, interface: Type[Any], implementation: Type[Any]) -> None:
    self._bindings[interface] = implementation
    
  def register_instance(self, interface: Type[Any], instance: Any) -> None:
    self._instances[interface] = instance
    
  def resolve(self, cls: Type[T]) -> T:
    if cls in self._instances:
      return self._instances[cls]

    target_cls = self._bindings.get(cls, cls)
    sig = inspect.signature(target_cls.__init__)
    dependencies: list[Any] = []

    for name, param in list(sig.parameters.items())[1:]:
      if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
        continue
      
      if param.annotation is inspect.Parameter.empty:
        raise Exception(f"Missing type annotation for {name} in {target_cls.__name__}")
      dep_instance = self.resolve(param.annotation)
      dependencies.append(dep_instance)

    instance = target_cls(*dependencies)
    self._instances[cls] = instance
    return instance
  
  def build(self, cls: Type[T]) -> T:
    if not is_dataclass(cls):
      raise TypeError(f"{cls.__name__} must be a dataclass")
    
    dependencies: dict[str, Any] = {}
    for name, field_type in cls.__annotations__.items():
      dependencies[name] = self.resolve(field_type)

    return cast(T, cls(**dependencies))