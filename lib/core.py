from .plp_types import Float, Integer, ATOMS, String, py_to_plp_type, Null, PLPType, List, Boolean, HashMap, Vector, Symbol, Lambda
from .helper import are_numbers, are_strings, create_relative_path_for_file
from typing import Union, Callable, Any
import copy
import lib.exceptions as exceptions
import lib.printer as printer
import lib.reader as reader
import math
import time

Number = Integer | Float
Sequence = List | Vector

def check_enough_arguments(args_num: int, *args: PLPType) -> None:
  """
    internal function that demonstrates how one could handle error handling
    
    but it is too much work for project this small therefore only a handful of functions use it just to demonstrate its behavior
  """
  if args_num < len(args):
    raise exceptions.ArgumentCountError(f"too many arguments for operation '_' ({len(args)} instead of {args_num})")
  elif args_num > len(args):
    raise exceptions.ArgumentCountError(f"not enough arguments for operation '_' ({len(args)} instead of {args_num})")

def plus_sign(*items: ATOMS) -> Union[String, Integer, Float]:
  """
    takes variable number of arguments
    
    if all are numbers, it returns their sum as either integer or float
    
    if all are string, it returns their concanation
    
    @examples
    - `(+ 3 8 1)` -> `12`
    - `(+ 3.0 7)` -> `10`
    - `(+ "hello" " world")` -> `"hello world"`
    - `(+ "hello" 123)` -> error
  """
  if are_numbers(*items):
    return py_to_plp_type(sum(items)) # type: ignore
  if are_strings(*items):
    return String("".join(items)) # type: ignore
  raise TypeError("+")

def number_subtraction(*items: ATOMS) -> Union[Integer, Float]:
  """
    subtracts two tumbers from each other
    
    returns interger if both were integer or float if at least one them is float (even though it could be integer)
    
    @examples
    - `(- 10 5)` -> `5`
    - `(- 10.0 5)` -> `5.0`
    - `(- 1.23 1)` -> `0.23`
  """
  if are_numbers(*items):
    check_enough_arguments(2, *items)
    return py_to_plp_type(items[0] - items[1]) # type: ignore
  raise TypeError("-")

def asterisk_sign(*items: ATOMS) -> Union[String, Integer, Float]:
  """
    it can either be n numbers (floats, ints, doesnt matter) and returns their product
    
    or it expects one integer N and one string and repeats that string N-times
    
    @examples
    - `(* 3 2)` -> `6`
    - `(* 3 (+ 2 2))` -> `12`
    - `(* 3 "foo")` -> `"foofoofoo"`
    - `(* 0 "hello world")` -> `""`
  """
  if are_numbers(*items):
    return py_to_plp_type(math.prod(items)) # type: ignore
  elif len(items) == 2 and isinstance(items[0], Integer) and isinstance(items[1], String):
    return String(items[0] * items[1])
  raise TypeError("*")

def division_sign(*items: ATOMS) -> Float:
  """
    expects 2 numbers, always returns a float (even though it could be integer)
    
    @examples
    - `(/ 10 2)` -> `5.0`
    - `(/ 21 2)` -> `10.5`
  """
  if are_numbers(*items):
    check_enough_arguments(2, *items)
    if items[1] == 0:
      raise ZeroDivisionError
    # items are either integer or float in this case
    return Float(items[0] / items[1]) # type: ignore
  raise TypeError("/")

def modulo_sign(a: Integer, b: Integer) -> Integer:
  """
    wrapper for the python `%` operator
    
    takes 2 integers, returns `a % b`
    
    @examples
    - `(% 100 4)` -> `0`
    - `(% 4 17)` -> `4`
  """
  return Integer(a % b)

def pr_str(*args: PLPType) -> String:
  """
    accepst variable number of arguments, parses them all as string and returns their concanation
    
    separated by empty space
    
        @example
    - `(pr-str 9 1 1)` -> `"9 1 1"`
    - `(pr-str (list 1 4 2) "hello world" (do (+ 10 20)))` -> `"(1 4 2) \"hello world\" 30`
  """
  return String(printer.format_sequence([arg for arg in args]))

def do_str(*args: PLPType) -> String:
  """
    accepst variable number of arguments, parses them all as string and returns their direct concanation
    
    @example
    - `(str 9 1 1)` -> `"911"`
    - `(str (list 1 4 2) "hello world" (do (+ 10 20)))` -> `"(1 4 2)hello world30`
  """
  return String(printer.format_sequence([arg for arg in args], "", False))

def prn(*args: PLPType) -> Null:
  """
    accepts variable number of arguments, prints all of them on one line, separated by empty space
    
    strings are printed surrounded by ""
    
    @example
    - `(prn 9 1 1)` -> `nil` (but prints out `9 1 1`)
    - `(prn (list 1 4 2) "hello world" (do (+ 10 20)))` -> `nil` (but prints out `(1 4 2) "hello world" 30`)
  """
  print(printer.format_sequence([arg for arg in args]))
  return Null()

def println(*args: PLPType) -> Null:
  """
    accepts variable number of arguments, prints all of them on one line, separated by empty space
    
    strings are printed without being surrounded by ""
    
    @example
    - `(println 9 1 1)` -> `nil` (but prints out `9 1 1`)
    - `(println (list 1 4 2) "hello world" (do (+ 10 20)))` -> `nil` (but prints out `(1 4 2) hello world 30`)
  """
  print(printer.format_sequence([arg for arg in args], " ", False))
  return Null()

# endless arguments, groups them to a list that is then returned
def to_list(*args: PLPType) -> List:
  """
    returns a list containing all given arguments
    
    @examples
    - `(list)` -> `()`
    - `(list 1 23 4)` -> `(1 23 4)`
    - `(list (do 1 2 3))` -> `3`
  """
  return List(list(args))

def to_vector(*args: PLPType) -> Vector:
  """
    returns a vector containg all given arguments
    
    @examples
    - `(vector)` -> `[]`
    - `(vector 1 2 3)` -> `[1 2 3]`
  """
  return Vector(list(args))

def count_items(sequence: PLPType) -> Integer:
  """
    returns the length of a sequence
    
    @examples
    - `(count (range 1 10 2))` -> `5`
    - `(count [])` -> `0`
    - `(count)` -> error
    - `(count "hello world")` -> 0
  """
  if isinstance(sequence, (List, Vector)):
    return Integer(len(sequence))
  return Integer(0)
  
def eq(arg1: PLPType, arg2: PLPType) -> Boolean:
  """
    checks whether both arguments are equal as in type and in deep children
    
    @examples
    - `(= 10 "10")` -> `false`
    - `(= 5 (+ 3 2))` -> `true`
    - `(= {a (list 1 2 3) b "foo"} {a [1 2 3] b "foo"})` -> `false`
  """
  if isinstance(arg1, Null) and isinstance(arg2, Null):
    return Boolean(True)

  if isinstance(arg1, (List, Vector)) and isinstance(arg2, (List, Vector)):
    return Boolean(len(arg1) == len(arg2) and all(eq(a, b) for a, b in zip(arg1, arg2)))

  return Boolean(arg1 == arg2 and type(arg1) is type(arg2))

def less_than(a: Number, b: Number) -> Boolean:
  """
    checks if `a` is less than `b`
    
    @example
    - `(< 10 10)` -> `false`
  """
  return Boolean(a < b)

def less_than_or_equal(a: Number, b: Number) -> Boolean:
  """
    checks if `a` is less than or equal to `b`
    
    @example
    - `(<= 10 10)` -> `true`
  """
  return Boolean(a <= b)

def greater_than(a: Number, b: Number) -> Boolean:
  """
    checks if `a` is greater than `b`
    
    @example
    - `(> 4 5)` -> `false`  
  """
  return Boolean(a > b)

def greater_than_or_equal(a: Number, b: Number) -> Boolean:
  """
    checks if `a` is greater than or equal to `b`
    
    @example
    - `(>= 10 5)` -> `true`
  """
  return Boolean(a >= b)

def slurp(file_name: String) -> String:
  """
    opens file given by path as the functions argument
    
    the path is relative to the main script location
    
    returns the file contents as string
  """
  file_path = create_relative_path_for_file(file_name)
  file = open(file_path)
  contents = file.read()
  file.close()
  return String(contents)

def prepend(new_el: PLPType, given_list: Sequence) -> List:
  """
    returns a list where a given element is prepended to the given list
        
    @params
    - `new_el`: element to be preprended to a list
    - `given_list`: the list to which the element should be prepended
    
    @example
    - `(prepend (list 1 2 3) [4])` -> `((1 2 3) 4)`
  """
  copied_list = copy.deepcopy(given_list)
  copied_list.insert(0, new_el)
  return List(copied_list)

def append(new_el: PLPType, given_list: Sequence) -> List:
  """
    returns a list where a given element is appended to the given list
        
    @params
    - `new_el`: element to be appended to a list
    - `given_list`: the list to which the element should be appended
    
    @example
    - `(append (list 1 2 3) [4])` -> `(4 (1 2 3))`
  """
  copied_list = copy.deepcopy(given_list)
  copied_list.append(new_el)
  return List(copied_list)

def concat(*given_lists: list[Sequence]) -> List:
  """
    returns list that is a concanation of all given lists
    
    if zero lists ares given, returns empty list
  
    @params (optional)
    - `*given_lists`: n number of list that will get concanated together
    
    @examples
    - `(concat (list 3 9 1) (list "hi" (do (define a 8) a)) [])` -> `(3 9 1 "hi" 8)`
    - `(concat)` -> `()`
  """
  concanated_lists = List([])
  for given_list in given_lists:
    concanated_lists.extend(given_list)
  return concanated_lists

def vec(sequence: Sequence) -> Vector:
  """
    transforms list into a vector with same elements
    
    given vector stays a vector
    
    @params
    - `sequence`: to be transformed into a vector
    
    @examples
    - `(vec (list 1 "hello" 0))` -> `[1 "hello" 0]`
    - `(vec [1 2 3])` -> `[1 2 3]`
  """
  return Vector(sequence)

def nth(index: Integer, sequence: Sequence):
  """
    returns the n-th element of a sequence
    
    if it's not defined, it raises and exception
    
    @params
    - `index`: the position of an element to be retrieved from a sequence, starts at `0` for the first element, negative values go from the back: `-1` for the last element
    
    @examples
    - `(nth 4 (list 1 2 3))` -> raises an `exception`
    - `(nth 2 (list 1 2 3))` -> `3`
    - `(nth -2 (list 1 2 3 4 5 6))` -> `5`
    - `(nth -1 ())` -> raises an `exception`
  """
  if index >= len(sequence) or len(sequence) + index < 0:
    raise Exception(f"can't acces sequenc at position {index} (out of bounds)")
  if index >= 0:
    return sequence[index]
  return sequence[len(sequence) + index]

def first(sequence: Sequence):
  """
    returns the first element of a sequence
    
    if sequence is empty, returns `nil`
    
    @params
    - `sequence`: the sequence from which the first element is returned
    
    @example
    - `(first (list 1 2 3))` -> `1`
  """
  if len(sequence) == 0:
    return Null()
  return sequence[0]

def last(sequence: Sequence):
  """
    returns the last element of a sequence
    
    if sequence is empty, returns `nil`
    
    @params
    - `sequence`: the sequence from which the last element is returned
    
    @example
    - `(last [1 2 (do (define a (- 10 13)) a)])` -> `-3`
  """
  if len(sequence) == 0:
    return Null()
  return sequence[len(sequence) - 1]

def splice(starting_index: Integer, ending_index: Integer, sequence: Sequence) -> Sequence:
  """
    reduces a sequence to given bounds, always returns a list
    
    if bounds overlap, raises an exception
    
    if indexes match, returns sequence of given type with single element
    
    @params
    - `starting_index`: starts at `0`, goes up
    - `ending_index`: can either be a negative number (then it starts at `-1`, goes down) or a positive (starting at 0) where it designates the ending index
    
    @examples
    - `(splice 0 -1 [1 2 3])` -> `(1 2)`
    - `(splice 0 2 [1 2 3 4 5])` -> `(1 2)`
    - `(splice 1 1 (list 0 2 3 4))` -> `()`
    - `(splice 1 2 (list 0 2 3 4))` -> `(2)`
    - `(spliec 1 3 (list 0 2 3 4))` -> `(2 3)`
    - `(splice 3 -2 (range 1 10))` -> `(4 5 6 7)`
  """
  ending_rescaled = ending_index if ending_index > 0 else len(sequence) + ending_index
  if starting_index > ending_rescaled or starting_index < 0 or (ending_rescaled >= len(sequence) and ending_rescaled != 0):
    raise SyntaxError("can't splice given sequence (out of bounds)")
  return List(sequence[starting_index:ending_index])

def take(length: Integer, sequence: Sequence) -> List:
  """
    returns a list containing the first n elements of given sequence where n is the provided length
    
    if length zero, zeturns empty sequence
    
    @params
    - `length`: starts at `0`, goes up
    - `sequence`
    
    @examples
    - `(take 2 (list 1 2 3 4 5))` -> `(1 2)`
    - `(take 3 [1 2 3 4 5 6])` -> `(1 2 3)`
  """
  return List(sequence[:length])

def split_string(separator: String, string: String) -> List:
  """
    splits string with provided separator into a list
    
    @params
    - `separator`
    - `string`
    
    @examples
    - `(split ";" "hello;world")` -> `("hello" "world")`
    - `(split "" "abc")` -> `("a" "b" "c")
    - `(split " " "lisp")` -> ("lisp")
  """
  if separator == "":
    result = list(string)
  else:
    result = string.split(separator)
  return List(map(lambda x: String(x), result))

def create_range(start: Integer, end: Integer, step: Integer = Integer(1)) -> List:
  """
  wrapper for python range()
  
  returns a list
  
  @params
  - `start`: included
  - `end`: excluded
  - `step` (optional): defaults to `1`
  
  @examples
  - `(range -1 4)` -> `(-1 0 1 2 3)`
  - `(range 3 9 2)` -> `(3 5 7)`
  - `(range 11 7)` -> `()`
  """
  return List(map(lambda x: Integer(x), range(start, end, step)))

def is_list(*args: PLPType) -> Boolean:
  """
    accepts variable list of arguments of any type, checks if all of them are list, in that case returns true otherwise false
    
    @examples
    - `(list? 4 (list 1 2 34))` -> `false`
    - `(list? () (list 4 1 ))` -> `true`
  """
  if len(args) == 0: return Boolean(False)
  for arg in args:
    if not isinstance(arg, List):
      return Boolean(False)
  return Boolean(True)

def is_sequence_empty(*args: PLPType) -> Boolean:
  """
  sequence is either list, vector or hashmap
  
  we need only one argument and that is the sequence we want to investigate
  """
  check_enough_arguments(1, *args)
  seq = args[0]
  if isinstance(seq, (List, Vector)):
    return Boolean(len(seq) == 0)
  elif isinstance(seq, HashMap):
    return Boolean(len(seq.map) == 0)
  # BUG: should probably be handled better
  #      instead of returning false, alarm the user that the function cant be used on this type
  return Boolean(False)

"""
  i think these functions speak for themselves
"""
def is_symbol(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, Symbol))
def is_nil(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, Null))
def is_string(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, String))
def is_true(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, Boolean) and expr == Boolean(True))
def is_false(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, Boolean) and expr == Boolean(False))
def is_number(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, (Integer, Float)))
def is_int(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, Integer))
def is_float(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, Float))
def is_function(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, (type(lambda: None), Lambda)))
def is_hashmap(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, HashMap))
def is_sequence(expr: Any) -> Boolean:
  return Boolean(isinstance(expr, Sequence))

def create_hashmap(*args: PLPType) -> HashMap:
  """
    takes even number of arguments and creates hash map from them
    
    wrapper for the '{}' syntax
    
    @params
    - `args`: expects variable but even number of key-values that create pairs
    
    @examples
    - `(hash-map "a" 1 "b" 3)` -> `{"a" 1 "b" 3}`
    - `(hash-map a 10)` -> raises and error because `a` is not defined by default
        - that's the difference from `{a 10}` -> `{a 10}`
        - i'm not actually sure which of these is the 'correct' implementation
  """
  return HashMap(list(args))

# BUG: `assoc` doesn't check the type of keys, so it might try to insert forbidden key type into hashmap
def assoc(hashmap: HashMap, *args: PLPType) -> HashMap:
  """
    returns new hashmap that merges proved hashmap with new key-value pairs as args
    
    @params
    - `hashmap`
    - `args`: expects variable but even number of key-values that create pairs
    
    @examples
    - `(assoc {"hello" "world"} "foor" "bar")` -> `{"hello" "world" "foo" "bar"}`
    - it doesn't mutate given hashmap
        - `(define a {"hello" "world"})`
        - `(assoc a "foo" "bar")` -> `{"hello" "world" "foo" "bar"}`
        - `a` stays `{"hello" "world"}`
  """
  new_hashmap = copy.deepcopy(hashmap)
  for i in range(0, len(args) -1, 2):
    new_hashmap.update(args[i], args[i + 1]) # type: ignore
  return new_hashmap
  
def dissoc(hashmap: HashMap, *keys: ATOMS) -> HashMap:
  """
  removes provided keys from provided hashmap
  
  if key isn't present in hashmap, doesn't raise and exception
  
  @params
  - `hashmap`
  - `keys`: can be empty
  
  @examples
  - `(dissoc {"foo" "bar" "one" "two" 3 4} "one" "foo")` -> `{3 4}`
  - `(dissoc {"hello" "world" 1 2} "foo" 1)` -> `{"hello" "world"}`
  - `(dissoc {"some" "hashmap"})` -> `{"some" "hashmap"}`
  """
  new_hashmap = copy.deepcopy(hashmap)
  for key in keys:
    new_hashmap.remove(key)
  return new_hashmap

def is_in_hashmap(key: ATOMS, hashmap: HashMap) -> Boolean:
  """
    checks if provided key is in hashmap
    
    @examples
    - `(contains? 1 {1 2 3 4})` -> `true`
    - `(contains? 4 {3 4})` -> `false`
  """
  return Boolean(key in hashmap.map)

def get_from_hashmap(key: ATOMS, hashmap: HashMap) -> PLPType:
  """
    retrieves a key from provided hashmap, if key not present in hashmap, returns `nil`
    
    @examples
    - `(get 1 {1 2 3 4})` -> `2`
    - `(get 2 {1 2 3 4})` -> `nil`
  """
  return hashmap.map.get(key, Null())

def get_hashmap_keys(hashmap: HashMap) -> List:
  """
    returns a list containig all keys in provided hashmap
    
    @examples
    - `(keys {1 2 3 4})` -> `(1 3)`
    - `(keys {})` -> `()` 
  """
  return List(hashmap.map.keys())
  
def get_hashmap_vals(hashmap: HashMap) -> List:
  """
    returns a list containing all valeus in provided hashmap
    
    @examples
    - `(vals {1 2 3 4})` -> `(2 4)`
    - `(vals {})` -> `()`
  """
  return List(hashmap.map.values())

def get_current_time() -> Integer:
  """
    returns elapsed time since the epoch in nanoseconds
  """
  return Integer(time.time_ns())

def get_type(expr: Any) -> String:
  """
    returns the type of given expression as string
    
    @examples
    - `(type (list 1 2 3))` -> `"List"`
    - `(type (time-ms))` -> `"Integer"`
  """
  return String(type(expr).__name__)
  
def floor(num: Number) -> Integer:
  """
    rounds provided number rounded down as an integer
    
    @examples
    - `(floor 8.4231)` -> `8`
    - `(floor 10)` -> `10`
  """
  return Integer(math.floor(num))

def join(separator: String, seq: Sequence) -> String:
  """
    joins elements of a sequence into a single string, separated by the provided separator
    
    @params
    - `separator`: the string to insert between each element
    - `seq`: sequence of elements to be joined
    
    @examples
    - `(join ", " (list "hello" "foo" "bar"))` -> `"hello, foo, bar"`
    - `(join "-" [1 2 3])` -> `"1-2-3"`
  """
  return String(separator.join(do_str(a) for a in seq))

# TODO: figure out how to efficiently check for required number of arguments in a function
ns: dict[str, Callable[..., PLPType]] = {
  "+": plus_sign,
  "-": number_subtraction,
  "*": asterisk_sign,
  "/": division_sign,
  "%": modulo_sign,
  "=": eq,
  ">=": greater_than_or_equal,
  ">": greater_than,
  "<=": less_than_or_equal,
  "<": less_than,
  "append": append,
  "assoc": assoc,
  "dissoc": dissoc,
  "concat": concat,
  "contains?": is_in_hashmap,
  "count": count_items,
  "empty?": is_sequence_empty,
  "false?": is_false,
  "first": first,
  "float?": is_float,
  "floor": floor,
  "fn?": is_function,
  "get": get_from_hashmap,
  "hash-map": create_hashmap,
  "hash-map?": is_hashmap,
  "int?": is_int,
  "join": join,
  "keys": get_hashmap_keys,
  "last": last,
  "list": to_list,
  "list?": is_list,
  "nil?": is_nil,
  "nth": nth,
  "number?": is_number,
  "prepend": prepend,
  "println": println,
  "prn": prn,
  "pr-str": pr_str,
  "range": create_range,
  "read-string": reader.read_raw_string,
  "seq?": is_sequence,
  "slurp": slurp,
  "splice": splice,
  "split": split_string,
  "str": do_str,
  "string?": is_string,
  "symbol?": is_symbol,
  "take": take,
  "time": get_current_time,
  "true?": is_true,
  "type": get_type,
  "vals": get_hashmap_vals,
  "vec": vec,
  "vector": to_vector,
}