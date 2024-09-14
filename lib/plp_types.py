from dataclasses import dataclass
from .exceptions import UndefinedPLPTypeError
from .env import Env
from itertools import combinations
from typing import Union, Any, Callable

class Integer(int): pass
class Float(float): pass
  
class Boolean:
  def __init__(self, boo: bool):
    self.boo = boo
  def __str__(self) -> str:
    if self.boo:
      return "true"
    return "false"
  def __eq__(self, other: Any) -> bool:
    return self.boo == other

class String(str): pass
class Symbol(str): pass
class Null: pass
class Comment: pass
class Keyword(str): pass

ATOMS = Union[Integer, Float, Boolean, Symbol, String, Keyword, Null, Comment]

class List(list["PLPType"]): pass

class Vector(list["PLPType"]): pass

class HashMap:
  def __init__(self, items: list["PLPType"]):
    hashmap = {}
    if len(items) % 2 != 0:
      raise SyntaxError("can't initialize hashmap with empty value")
    for key in items[0::2]:
      if not isinstance(key, (Keyword, String, Integer, Float)):
        raise SyntaxError(f"can't have key of type '{type(key).__name__}' in a hashmap")
    for (key1, key2) in combinations(items[0::2], 2):
      if key1 == key2 and type(key1) is type(key2):
        raise SyntaxError(f"can't initialize hashmap with two or more same keys: '{key1}'")
    for i in range(0, len(items) - 1, 2):
      hashmap[items[i]] = items[i + 1]
    self.map: dict[ATOMS, "PLPType"] = hashmap
  def items(self) -> list[tuple[ATOMS, "PLPType"]]:
    return list(self.map.items())
  # BUG: update function could use some error checking
  def update(self, key: ATOMS, val: "PLPType") -> None:
    self.map[key] = val
  def remove(self, key: ATOMS) -> None:
    if key in self.map:
      del self.map[key]
  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, HashMap):
      return False
    return self.map == other.map

PLPType = Union[ATOMS, List, Vector, HashMap, "Lambda", Callable[..., "PLPType"]]
@dataclass
class Lambda:
  ast: PLPType
  get_env: Callable[[list[PLPType]], Env]

def is_defined_or_true(arg: PLPType) -> bool:
  return not (isinstance(arg, Null) or (arg == False and isinstance(arg, Boolean)))

def is_function(possible_function: Any) -> bool:
  return isinstance(possible_function, type(lambda: None))

def py_to_plp_type(var: Any) -> PLPType:
  if isinstance(var, int): return Integer(var)
  elif isinstance(var, float): return Float(var)
  raise UndefinedPLPTypeError(var)
