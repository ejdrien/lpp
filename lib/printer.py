import lib.plp_types as plp
from .plp_types import PLPType
from types import FunctionType

def print_ast(ast: PLPType | FunctionType, print_readably: bool = True) -> None:
  print(format(ast, print_readably))

def format(ast: PLPType | FunctionType, print_readably: bool = True) -> str:
  match ast:
    case plp.List():
      return f"({format_sequence(ast, " ", print_readably)})"
    case plp.Vector():
      return f"[{format_sequence(ast, " ", print_readably)}]"
    case plp.HashMap():
      items = [f"{format(key, print_readably)} {format(value, print_readably)}" for key, value in ast.map.items()]
      return "{" + " ".join(items) + "}"
    case plp.Integer():
      return str(ast)
    case plp.Float():
      return str(ast)
    case plp.Boolean():
      return str(ast)
    case plp.String():
      if print_readably:
        s = ast.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f"\"{s}\""
      else:
        return f"{ast}"
    case plp.Null():
      return "nil"
    case plp.Comment():
      return ""
    # BUG: když se nepoužitej formatter v exceptions, keywordy se nevytisknout s :
    case plp.Keyword():
      return ":" + ast
    case plp.Symbol():
      return ast
    case plp.Lambda():
      return "#<lambda>"
    # i'm matching against classes and since we have predefined functions in the core file then only those will end up here
    case _:
      return f"#<function '{ast.__name__}'>"

def format_sequence(sequence: plp.List | plp.Vector | list[PLPType], separator: str = " ", print_readably: bool = True) -> str:
  return separator.join(format(a, print_readably) for a in sequence)