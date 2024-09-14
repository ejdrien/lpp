class UndefinedSymbolError(Exception): pass
class UndefinedPLPTypeError(Exception): pass
class ArgumentCountError(Exception): pass

RED = "\033[91m"
RESET = "\033[0m"

def handle_exception(exception: Exception) -> None:
  match exception:
    case TypeError():
      print(f"{RED}[type error]: can't perform operation \"{exception}\" on different types", RESET)
    case UndefinedSymbolError():
      print(f"{RED}[undefined symbol]: '{exception}' not found", RESET)
    case UndefinedPLPTypeError():
      print(f"{RED}[undefined plp type]: {exception}", RESET)
    case ArgumentCountError():
      print(f"{RED}[argument count error]: {exception}", RESET)
    case SyntaxError():
      print(f"{RED}[syntax error]: {exception}", RESET)
    case ZeroDivisionError():
      print(f"{RED}[math error]: you sadly can't divide by zero", RESET)
    case EOFError():
      print(f"{RED}[unmatched]:", exception, RESET)
    case _:
      print(f"{RED}[error]: {exception}", RESET)