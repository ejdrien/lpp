from .helper import is_float, is_int, is_string
from .plp_types import Integer, Symbol, List, Float, Boolean, Vector, HashMap, PLPType, String, Keyword, Null, ATOMS
from typing import Optional
import re

class Reader:
  """
    Reader class stores tokens which are used to construct an AST
  """
  def __init__(self, tokens: list[str]):
    self.tokens = tokens
    self.position = 0

  def next(self) -> Optional[str]:
    if self.position < len(self.tokens):
      token = self.tokens[self.position]
      self.position += 1
      return token
    return None

  def get(self) -> Optional[str]:
    if self.position < len(self.tokens):
      return self.tokens[self.position]
    return None

def read_raw_string(input: str) -> PLPType:
  """
    reads raw string and returns it's AST (abstract-syntax-tree) form using PLP syntax
  """
  tokens = tokenize(input)
  if len(tokens) == 0:
    raise Exception("empty line!")
  reader = Reader(tokens)
  return read_token(reader)
  
def tokenize(body: str) -> list[str]:
  """
    splits raw string into specific pre-defined segments (using a given regular expression) that can be then further evaluated
  """
  # source https://norvig.com/lispy2.html
  pattern = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)""")
  return [token for token in pattern.findall(body) if token.strip()]

def read_token(reader: Reader) -> PLPType:
  """
    transforms a token into it's PLP internal representation
  """
  token = reader.get()
  assert token is not None
  # BUG: if comment is the last token, it throws error as undefined symbol
  #      i honestly don't the what's the best solution here so i'm leaving this open
  if token[0] == ";":
    reader.next()
    return read_token(reader)
  match token:
    # quote
    case "\'":
      reader.next()
      return List([Symbol("quote"), read_token(reader)])
    # could be expanded to parse quasiquote, unquote, ...
    # beginning of a list expression
    case "(":
      return read_list(reader)
    case ")":
      raise EOFError('unexpected ")"')
    # beginning of a vector
    case "[":
      return read_vector(reader)
    case "]":
      raise EOFError('unexpected "]"')
    # beginning of a hash map
    case "{":
      return read_hash_map(reader)
    case "}":
      raise EOFError('unexpeced "}"')
    case _:
      return read_atom(reader)


def read_sequence(reader: Reader, end: str) -> list[PLPType]:
  """
    handles tokens that are a sequence denoted by specific symbol `end`
  """
  result: list[PLPType] = []
  token = reader.next()
  while True:
    token = reader.get()
    if token == end:
      reader.next()
      break
    if token is None:
      raise EOFError(f'missing closing "{end}"')
    result.append(read_token(reader))
  return result

def read_list(reader: Reader) -> List:
  return List(read_sequence(reader, ")"))

def read_vector(reader: Reader) -> Vector:
  return Vector(read_sequence(reader, "]"))

def read_hash_map(reader: Reader) -> HashMap:
  return HashMap(read_sequence(reader, "}"))

def read_atom(reader: Reader) -> ATOMS:
  token = reader.get()
  assert token is not None
  if is_int(token):
    token = Integer(int(token))
  elif is_float(token):
    token = Float(float(token))
  elif is_string(token):
    string = token[1:-1].replace('\\\\', '\b').replace('\\"', '"').replace('\\n', '\n').replace('\b', '\\')
    token = String(string)
  elif token[0] == "\"":
    raise EOFError("expected closing '\"'")
  elif token[0] == ":":
    token = Keyword(token[1:])
  elif token == "true":
    token = Boolean(True)
  elif token == "false":
    token = Boolean(False)
  elif token == "nil":
    token = Null()
  else:
    token = Symbol(token)
  reader.next()
  return token