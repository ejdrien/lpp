from lib.helper import create_relative_path_for_file
from lib.rep import rep
import atexit
import lib.exceptions as exceptions
import os
import lib.printer as printer
import readline
import sys

def main() -> None:
  if len(sys.argv) > 1:
    non_existent_files: list[str] = []
    for file_path in sys.argv[1:]:
      if not os.path.isfile(create_relative_path_for_file(file_path)):
        non_existent_files.append(file_path)
    if non_existent_files:
      print(
        "\033[91m",
        "[invalid file paths]: the following files do not exist: ",
        ", ".join(non_existent_files),
        "\033[0m",
        sep=""
      )
      sys.exit(1)

    file_paths = map(lambda x: create_relative_path_for_file(x), sys.argv[1:])
    for file_path in file_paths:
      try:
        rep(f"""(load-file "{file_path}")""")
      except Exception as e:
        exceptions.handle_exception(e)
        sys.exit(1)
    sys.exit(0)
    
  # register cmd history
  histfile = os.path.join(os.path.expanduser("~"), ".plp-history")
  try:
    readline.read_history_file(histfile)
  except Exception:
    pass
  readline.set_history_length(1000)
  atexit.register(readline.write_history_file, histfile)
  
  while True:
    try:
      printer.print_ast(rep(input("plp> ")))
    except Exception as e:
      exceptions.handle_exception(e)

if __name__ == "__main__":
  main()