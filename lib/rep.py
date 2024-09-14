from lib.env import Env
from lib.plp_types import PLPType
from lib.eval import EVAL, EVAL_RETURN_TYPE
import lib.core as core
import lib.plp_types as plp
import lib.reader as reader

global_environment = Env()
for symbol, value in core.ns.items():
  global_environment.set(plp.Symbol(symbol), value)

# BUG? this takes the global envinronment
#      but if i want to use eval within some other env
#      it won't work, could be handy to expand the behavior
#      or define something liike `local_eval_func`
def eval_func(ast: PLPType) -> EVAL_RETURN_TYPE:
  return EVAL(ast, global_environment)
global_environment.set(plp.Symbol("eval"), eval_func)

def rep(arg: str) -> PLPType:
  return EVAL(reader.read_raw_string(arg), global_environment)

rep("(define not (fn (a) (if a false true)))")
rep(f"""(define load-file (fn (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))""")
rep("(define time-ms (fn () (floor (/ (time) 1e6))))")
rep(f"""(define length (fn (string) (count (split "" string))))""")
rep("(define ** (fn (a b) (if (= b 1) a (if (= b 0) 1 (* a (** a (- b 1)))))))")
rep("(define // (fn (a b) (floor (/ a b))))")