from typing import Any
from .plp_types import Integer, Float, String
import re
import os

def is_float(possible_float: Any) -> bool:
  try:
    float(possible_float)
    return True
  except:
    return False
  
def is_int(possible_int: Any) -> bool:
  try:
    int(possible_int)
    return True
  except:
    return False
  
def is_string(possible_string: Any) -> bool:
  # source: https://github.com/kanaka/mal/blob/master/process/guide.md
  string_re = re.compile(r'"(?:[\\].|[^\\"])*"')
  return bool(re.match(string_re, possible_string))

def are_numbers(*possible_nums: Any) -> bool:
  return all(isinstance(n, (Integer, Float)) for n in possible_nums)

def are_strings(*possible_strings: Any) -> bool:
  return all(isinstance(s, String) for s in possible_strings)

def create_relative_path_for_file(file_name: str) -> str:
  curr_dir = os.path.dirname(__file__)
  return os.path.join(curr_dir, "..", file_name)