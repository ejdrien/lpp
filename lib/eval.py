from lib.env import Env
from lib.plp_types import PLPType
from typing import Union, Callable
import lib.exceptions as exceptions
import lib.plp_types as plp

EVAL_RETURN_TYPE = Union[PLPType, Callable[..., PLPType]]

def EVAL(ast: PLPType, env: Env) -> EVAL_RETURN_TYPE:
  while True:
    match ast:
      # symbol denotes a value stored in env
      case plp.Symbol():
        symbol_value = env.get(ast)
        if symbol_value is None:
          raise exceptions.UndefinedSymbolError(ast)
        return symbol_value

      # vector is always just a list of different items
      # all items need to be evaluated on its own     
      case plp.Vector():
        return plp.Vector([EVAL(a, env) for a in ast])

      # hashmap is just a hashmap where keys are always static
      #                             and values are exprs that need to be evaluated
      case plp.HashMap():
        for key, value in ast.items():
          ast.update(key, EVAL(value, env))
        return ast

      # list is denoted like (symbol expr1 expr2 ...)
      # the first element is always a symbol that needs to be invoked with the remaining elements as its arguments
      case plp.List():
        if len(ast) == 0:
          return ast
        operator = ast[0]
        args = ast[1:]
        # environment-altering pre-defined operators
        if isinstance(operator, plp.Symbol):
          match operator:
            case "define":
              return eval_define(args, env)
            case "do":
              ast = eval_do(args, env)
              continue
            case "fn":
              return eval_fn(args, env)
            case "if":
              ast = eval_if(args, env)
              continue
            case "let*":
              ast, env = eval_let(args, env)
              continue
            case "while":
              pre_while_env = Env(env)
              eval_while(args, pre_while_env)
              for key in pre_while_env.data:
                if key in env.data:
                  env.set(key, pre_while_env.data[key])
              return plp.Null()
            # quoting is kinda broken, the cause rises from the reader implementation
            case "quote":
              return args[0]
            case _: pass # to satisfy type-checker

        # this can give us either a function from the environment or the 'first' value is defined as some arbitraty type such as integer etc. on which we can't apply the arguments per the definition of our list
        function = EVAL(operator, env)
        if plp.is_function(function):
          # if it passes the custom check, it must be Callable
          return function(*(EVAL(a, env) for a in args)) # type: ignore
        elif isinstance(function, plp.Lambda):
          ast = function.ast
          env = function.get_env([EVAL(a, env) for a in args])
          continue
        else:
          raise SyntaxError(f"'{operator}' is not a function; can't apply '{operator}' on given arguments")

      case _:
        return ast

def eval_define(args: list[PLPType], env: Env) -> EVAL_RETURN_TYPE:
  if len(args) != 2:
    raise SyntaxError(f"operator 'define' expects 2 arguments (got {len(args)})")

  key = args[0]
  if isinstance(key, plp.Symbol):
    value = EVAL(args[1], env)
    return env.set(key, value)
  elif isinstance(key, plp.Keyword):
    raise SyntaxError(f"operator 'define' can't use keyword ':{key}'")
  else:
    raise SyntaxError(f"operator 'define' can't redefine atom '{key}'")

def eval_let(args: list[PLPType], env: Env) -> tuple[PLPType, Env]:
  if len(args) != 2:
    raise SyntaxError(f"operator 'let*' expects 2 arguments (got {len(args)})")
  
  new_bindings = args[0]
  if not isinstance(new_bindings, plp.List):
    raise SyntaxError("operator 'let*' expects first paramater to be a list for bindings")
  
  local_env = Env(env)
  for i in range(0, len(new_bindings) - 1, 2):
    key = new_bindings[i]
    if isinstance(key, plp.Symbol):
      value = EVAL(new_bindings[i + 1], local_env)
      local_env.set(key, value)
    else:
      raise SyntaxError("operator 'let*' expects odd bindings to be a symbol")
  return args[1], local_env

def eval_do(args: list[PLPType], env: Env) -> PLPType:
  if len(args) == 0:
    raise SyntaxError("operator 'do' expects at least 1 argument (got 0)")

  for expr in args[:-1]:
    EVAL(expr, env)
  return args[-1]

def eval_if(args: list[PLPType], env: Env):
  if len(args) not in [2, 3]:
    raise SyntaxError(f"operator 'if' expects either 2 or 3 arguments (got {len(args)})")
  
  if_condition = EVAL(args[0], env)
  if plp.is_defined_or_true(if_condition):
    return args[1]
  elif len(args) == 3:
    return args[2]
  else:
    return plp.Null()

def eval_fn(args: list[PLPType], env: Env):
  if len(args) != 2:
    raise SyntaxError(f"operator 'fn' expects 2 arguments (got {len(args)})")
  
  fn_args = args[0]
  if not isinstance(fn_args, plp.List):
    raise SyntaxError("operator 'fn' expects arguments to be in a list")
  for arg in fn_args:
    if not isinstance(arg, plp.Symbol):
      raise SyntaxError(f"opeartor 'fn' expects arguments to not be atoms; found: {arg}")

  def get_env(exprs: list[PLPType]) -> Env:
    return Env(env, fn_args, exprs) # type: ignore
  return plp.Lambda(args[1], get_env)

def eval_while(args: list[PLPType], env: Env):
  if len(args) < 2:
    raise SyntaxError(f"operator 'while' expects at least 2 arguments (got {(len(args))})")
  
  while_condition = args[0]
  while plp.is_defined_or_true(EVAL(while_condition, env)):
    for expr in args[1:]:
      EVAL(expr, env)