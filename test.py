from lib.rep import rep
import lib.printer as printer
import os
import sys

RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"

TESTS_DIRECTORY = "tests"

def test(expression: str) -> str:
  return printer.format(rep(expression))

def run_tests_in_directory(show_failed: bool) -> None:
  if not os.path.isdir(TESTS_DIRECTORY):
    print(RED, f"[path error]: tests' directory '{TESTS_DIRECTORY}' doesn't exist", RESET)
    return

  test_files = [file for file in os.listdir(TESTS_DIRECTORY) if file.endswith(".plptest")]
  
  total_passed_tests: int = 0
  total_failed_tests: int = 0
  all_failed_tests: list[tuple[str, str, str]] = []
  
  for test_file in test_files:
    print(f"\nRunning tests in {BLUE}{test_file}{RESET}...")
    passed_tests, failed_tests, failed_details = run_tests(test_file)
    total_passed_tests += passed_tests
    total_failed_tests += failed_tests
    all_failed_tests.extend(failed_details)

  if total_failed_tests == 0:
    print({GREEN}, f"\nAll tests passed! Total tests: {total_passed_tests}", {RESET})
  else:
    print(RED, f"\nSome tests failed. Total passed: {total_passed_tests}, Total failed: {total_failed_tests}", RESET)
    if show_failed:
      print(RED, "\nSummary of failed tests:", RESET)
      for code, result, expected in all_failed_tests:
        print(RED, f"Test failed for code: {code}\n  Output: {result}\n  Expected: {expected}\n", RESET)

def run_tests(file_name: str) -> tuple[int, int, list[tuple[str, str, str]]]:
  test_file_path = os.path.join(TESTS_DIRECTORY, file_name)
  if not os.path.isfile(test_file_path):
    print(RED, f"Test file {test_file_path} does not exist.", RESET)
    return 0, 0, []

  with open(test_file_path) as file:
    lines: list[str] = file.readlines()

  passed_tests: int = 0
  failed_tests: int = 0
  failed_details: list[tuple[str, str, str]] = []
    
  i = 0
  while i < len(lines):
    line: str = lines[i].strip()
        
    if line.startswith(";;"):
      print(YELLOW, f"{line[2:].strip()}", RESET)
      i += 1
      continue
  
    if line and not line.startswith(";"):
      code: str = line
      expected_output: str = lines[i + 1].strip() if i + 1 < len(lines) else ""
      i += 1

      if expected_output.startswith(";err!"):
        try:
          test(code)
          failed_tests += 1
          failed_details.append((code, "no error raised", "expected error"))
          print(RED, f"[failed]  {code} -> no error raised (error expected)", RESET)
        except Exception:
          passed_tests += 1
          print(GREEN, f"[passed]  {code} -> error raised (error expected)", RESET)
      elif expected_output.startswith(";"):
        expected_output = expected_output[1:].strip()
        try:
          result: str = str(test(code))
          if result == expected_output:
            passed_tests += 1
            print(GREEN, f"[passed]  {code} -> {result} (expected: {expected_output})", RESET)
          else:
            failed_tests += 1
            failed_details.append((code, result, expected_output))
            print(RED, f"[failed]  {code} -> {result} (expected: {expected_output})", RESET)
        except Exception as e:
          failed_tests += 1
          failed_details.append((code, str(e), "unexpected error raised"))
          print(RED, f"[unexpected error]  {code} -> {repr(e)}", RESET)
      else:
        try:
          result: str = str(test(code))
          print(GREEN, f"[executed]  {code} -> {result}", RESET)
        except Exception as e:
          print(RED, f"[execution failed]  {code} -> {repr(e)}", RESET)

    i += 1

  print(f"\nSummary for {BLUE}{test_file_path}{RESET}: {passed_tests} passed, {failed_tests} failed.")
  return passed_tests, failed_tests, failed_details

def main():
  show_failed_tests = "--show-failed" in sys.argv
  if len(sys.argv) > 1 and not show_failed_tests:
    run_tests(sys.argv[1])
  else:
    run_tests_in_directory(show_failed_tests)

if __name__ == "__main__":
  main()