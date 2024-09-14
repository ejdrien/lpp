from __future__ import annotations
from typing import Callable, Union, Optional, Self, TYPE_CHECKING
if TYPE_CHECKING:
  from .plp_types import PLPType, Symbol
  EXPR_TYPE = Union[PLPType, Callable[..., PLPType]]

class Env:
  """
    class that represents plp envinronemnt
    
    there is a global one and local ones inside functions, while loops, ...
    
    getting from environment firstly checks its own then reaches out to outer envs
    
    but editing an env is immutable meaning that outer can never be reached but only read
  """
  def __init__(self, outer: Optional[Self] = None, binds: Optional[list[Symbol]] = None, exprs: Optional[list[EXPR_TYPE]] = None):
    self.data: dict[Symbol, EXPR_TYPE] = dict()
    self.outer: Optional[Self] = outer
    if binds is not None and exprs is not None:
      for (bind, expr) in zip(binds, exprs):
        self.set(bind, expr)

  def set(self, key: Symbol, value: EXPR_TYPE) -> EXPR_TYPE:
    self.data[key] = value
    return value

  def get(self, key: Symbol) -> Optional[EXPR_TYPE]:
    value = self.data.get(key)
    if value is None:
      if self.outer is None:
        return None
      else:
        return self.outer.get(key)
    else:
      return value