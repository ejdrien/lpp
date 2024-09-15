### Syntaxe PLP

Syntaxe vychází z klasického LISPovského zápisu. Člověk, který již má zkušenost s LISPem, by měl PLP kompletně rozumět a být schopný s ním pracovat. Jelikož já mám nulovou zkušenost s LISPem, u implementace některých částí jsem zvolil řešení, které mi přišlo pro danou funkcionalitu nejlepší, avšak může se lišít od standardní LISPovské praxe, a proto jsou zde všechny klíčové informace popsány tak, že jim porozumí i člověk bez předchozí znalosti LISPu.


#### Základ
Většina programovacích jazyků odděluje jednotlivé výrazy řádkami zakončemý středníky. PLP variantou je závorkování pomocí `()`. Výrazy vyžadují oddělení na novou řádku. Jakékoliv další znaky po ukončující závorce, která uzavírá první otevřenou závorku na rádce, budou ignorovány. Uvnitř výrazu nezálezí na whitespacu.Výrazy uvnitř dalších výrazů jsou oddělovány jednoduchou mezerou. Místo výrazů lze využít i komentářů, které začínají středníkem (`;`).
```lisp
(platný-výraz)
(další-platý výraz    ) toto celé bude vyignorované včetné (třeba-platného-výrazu)
; toto je komentář, který bude celý ignorován
(   platný-výraz (
  včetné-dalšího-platného-výrazu ; a jeho komentáře


  )    
  
)
```
Výraz v závorkách má přesně danou strukturu:
```lisp
(operátor operand1 operand2 ...)
```
`Operátor` je přesně předem zadefinovaná funkce, která pracuje s `operandy 1-n` jako svými argumenty. Například
```lisp
(+ 10 20) ; -> 30
(define foo "bar") ; -> uloží "bar" do 'foo'
(10 20 30) ; -> hodí chybu, neboť '10' není operátor
```
`Operátory` i `operandy` mohou být reprezentovány výrazy, které vrátí požadovaný typ.
```
(+ (- 10 5) (** 3 2)) ; -> 14
```
Chceme-li získat hodnotu proměnné, proměnnou nebudeme uzavírat do závorek. Je-li proměnná funkce, jejím uzavřením na první místě v závorce ji zavoláme. Proměnné mohou začínat pouze alfnumerický symboly (nealfanumerické jsou rezervované), avšak mohou uvnitř sebe obsahovat i nealfanumerické symboly. Lze zadefinovat dokonce na první pohled vyhrazené názvy jako proměnnou
```lisp
10 ; -> 10
"hello world" ; -> "hello world"
(define @foo "bar") ; -> chyba
(define abc@def "hi") ; -> uloží "hi" do abc@def
(define define 10) ; -> define bude dále fungovat, ale bude i proměnná 10
+ ; -> #<function 'plus_sign'>
(/ 10 2) ; -> zavolání / na 10 a 2, vrátí 5
```

#### Čísla
Číslo je buď reprezentováno jako `Integer` nebo `Float`. Jedná se o wrapper pythonovských typů. Lze kombinovat funkce mezi oběma typy.
```lisp
(+ 10 5.5) ; -> 15.5
(/ 21 2) ; -> 10.5
(// 27.0 5.0) ; -> 5
```

#### String
String je vždy uzavřen do dvojtých uvozovek (`""`).
```lisp
(+ "hello " "world") ; -> "hello world"
(* 3 "foo") ; -> "foofoofoo"
(str 10) ; -> "10"
```

#### Boolean
Jedná se buď o `true`, nebo `false`. Existuje pouze jeden logický operátor na Booleanech: `not`.
```lisp
(not true) ; -> false
(not false) ; -> true
```

#### nil
Prostě jen `nil`. Může sloužit jako alternativa k nedefinovaných výrazům, které v PLP nemají žádnou reprezentaci.
```lisp
(= nil false) ; -> false
(not nil) ; -> true
```

#### Symboly
V PLP je symbol všechno, co není žádným již jiným. Symboly se ukládájí proměnné a funkce. Je to například `+`, `/`, `list`, `count`, `foo`, `bar`, ...

Když PLP nerozpozná symbol (není uložený v daném prostředí), ukončí program s chybovou hláškou.

Symboly se používájí ryze jako názvy proměnných.
```lisp
(define foo "bar") ; -> "bar"
```

#### Keyword
Alternativa pro symboly, která má praktické využití jen v HashMapě jako identifikátor nějaké hodnoty.

Keywordy začínají dvojtečkou (`:`), po které následuje alfanumerický zápis.
```
:abc ; -> :abc
(define :abc 10) ; -> nelze
(list :a :b :c) ; -> (:a :b :c)
```

#### Pole
Pole je vnitřně reprezentováno jak `()`, tak i `[]`. Kulaté závorky utváří `List`, hranaté `Vector`. Rozdílem je, že `List` slouží primárně jako reprezentace výrazů a aplikace prvního členu na zbylé. `Vector` slouží jako (ve výsledku kompletně zbytečná) alternativa pro např. rychlejší definci polí nebo vizuální odlišení.

Výrazy jsou vždy od sebe oddělovány mezerou.

Většina funkcí, které pracuje s poli, většinou vrací `List`, i když přijímá `Vector` jako argument.
```lisp
[+ 1 2] ; -> vrátí [+ 1 2], uložené '+' zde reprezentuje uloženou funkci
(+ 1 2) ; -> 3
(list 1 2 3) ; -> (1 2 3)
(list [1 2 3]) ; -> ([1 2 3])
```

#### HashMap
Klasická HashMap, wrapper pro pythonovský `dict[Symbol, Any]`. Užívá `{}`. Jako `key` se doporučuje užít `Keyword`, ale lze užít i `String`, `Integer` a `Float`. Definuje se jako sudá posloupnost, kde liché členy jsou klíčem a následující člen je klíči přiřazená hodnota.
```lisp
{:a 10 :b 20} ; -> {:a 10 :b 20}
(hash-map 1 20 3 40) ; -> {1 20 3 40}
(define a {1 20 3 40 5 60}) ; -> {1 20 3 40 5 60}
(get 1 a) ; -> 20
(get 0 a) ; -> nil
(assoc a 7 80) ; -> {1 20 3 40 5 60 7 80}
(dissoc a 3 5) ; -> {1 20}
a ; -> {1 20 3 40 5 60}
```

#### Prostředí pozměňující funkce
PLP obsahuje pár funkcí, které nelze předefinovat a které nějakým způsobem ovlivňují prostředí, mají specifickou syntax.

##### `define`
Slouží jednoduše k přiřazování hodnot k daným symbolům neboli k ukládání proměnných. Argumetny `symbol` i `(expr)` jsou povinné. Vrací přiřazenou hodnotu.
```lisp
(define symbol (expr))
```
```lisp
(define foo "bar") ; foo -> "bar"
(define n (+ 10 20)) ; n -> 30
(prn (define a n)) ; -> 30
```

##### `do`
Vykoná v posloupnosti za sebou `(expr1)`, `(expr2)`, ... Je vyžadován alespoň jeden argument. Hodnotu posledního vrátí.
```lisp
(do (expr1) (expr2) ...)
```
```lisp
(do (define a 10) (+ a 20)) ; -> 30
(do (+ 20 30) (- 50 50) "hello world") ; -> "hello world"
```

##### `fn`
Vytvoří funkci, její uložení pro pozdější užití je však potřeba udělat pomocí `define`. Argument `(args)` musí být `List`, ve kterém jsem jednotlivé symboly reprezentující argumenty funkce – při pozdějším volání funkce jsou povinné jenom argumenty, které funkce využívá; nelze zaměňovat jejich pořadí. Společně s `(expr)` jsou to povinné argumenty `fn`.
```lisp
(fn (args) (expr))
```
```lisp
(define sum (fn (n) (* (// n 2) (+ n 1))))
(sum 100) ; -> 5050
(fn () "hello world") ; -> doesn't call function
(fn (doesnt matter how many args) "hello world") ; -> alternative definition
((fn () "hello world")) ; -> "hello world"
```

##### `if`
Klasický `if-statement`. Povinně vyžaduje `(condition)` a `(if-true)`. Argument `(if-false)` je volitelný. Je-li `(condition)` pravdivá, vrací hodnotu `(if-true)`, jinak vrací hodnotu `(if-false)`, pokud je zadefinováno, jinak vrátí `nil`.

Vyhodnocení `(condition)` je vesměs stejné jako to pythonovské (nepřekvapivě).
```lisp
(if (condition) (if-true) (if-false))
```
```lisp
(if true true false) ; -> true
(if nil true false) ; -> false
(if "" true false) ; -> true
(if "hi my name is" true false) ; -> true
(if (= 10 "10") true false) ; -> false
```

##### `let*`
Tato funkce vytvoří nové lokální prostředí a v něm je schopná vykonávat PLP kód. Prostředí je podřazené tomu okolnímu, tedy nově definované proměnné v něm zůstanu, lze získat hodnotu proměnných z okolí, ale nelze ji přepisovat.

Oba argumenty jsou povinné. Argument `(bindings)` je `List`, ve kterém jsou dvojice jako při definici HashMapy – liché jsou nově definované proměnné, sudé jejich hodnoty. A `(expr)` jich může následně využívat
```lisp
(let* (bindings) (expr))
```
```lisp
(define c 1) ; -> 1
(let* (c 2) c) ; -> 2
c ; -> 1
(let* (a 10) (+ a c)) ; -> 11
a ; -> chybová hláška: 'a' neexistuje

(let* (a 10) (do (define a 20) a)) ; -> 20
```

##### `'`
Funkce `'` neboli `quote` je vlastní LISPu. Jako argument bere nějaký výraz, který ale nevyvolá a vrací jeho podobu pro pozdější užití. Samo o sobě to není moc užitečné. Unikátnost a výhoda `quote` se ukazuje až v kombinaci s `quasiquote`, `unquote`, `def-macro` atd., což jsou funkce, které bohužel nejsou přítomny v PLP. Tato featura byla přidána jen jako proof-of-concept.

V PLP jde `quote` výraz vyvolat pouze užitím funkce `eval`, která však pracuje v globálním prostředí, tedy některá funkcionalita, jako je používání parametrů ve funkci, nebude fungovat.
```lisp
'(+ 1 2 3) -> (+ 1 2 3)
(define a '(+ 1 2 3)) ; -> (+ 1 2 3)
a ; -> (+ 1 2 3)
(eval a) ; -> 6

(define b '//) ; -> //
(eval b) ; -> #<lambda>
((eval b) 9 10) ; -> 0
```

##### `while`
Klasický `while` loop, který je schopný přepisovat vnější proměnné – jen pokud již byly zadefinované. Nově zadefinované budou použitelné pouze uvnitř daného `while` loopu a po jeho skončení zaniknou.

Argumenty `(condition)` a `(expr1)` jsou povinné, další jsou volitelné. Je-li `(condition)` pravdivá, spustí se `(expr1)`, `(expr2)`, ... popořadě. Na konci se znovu přehodnotí `(condition)`, dokud nepřestane být pravdivá. Sám o sobě vrací `nil`
```lisp
(while (condition) (expr1) (expr2) ...)
```
```lisp
(while true (println "hello world")) ; donekonečna bude vypisovat 'hello world'
; vypíše každé číslo od 1 do 10 (včetně) na samostatnou řádku
(let* (i 1)
  (while (< i 11)
    (println i)
    (define i (+ i 1))))
; vypíše každé číslo od 1 do 4 (včetně), ale 'i' zůstane po skončení nepozměněná
(define i 1)
(let* ()
  (while (< i 5)
    (println i)
    (define i (+ i 1))))
i ; -> 1
; vypíše každé číslo od 1 do 4 (včetně), ale 'i' po skončení bude pozměněné
(define i 1)
(while (< i 5)
  (println i)
  (define i (+ i 1)))
i ; -> 5
```

#### Další předdefinované funkce
V souboru `lib/core.py` je zadefinovano mnoho funkcí, které dovolují s PLP řešit nějaké základní problémy. Pár funkcí je zadefinovaných v samotné PLP syntaxi v souboru `lib/rep.py`.

Následuje stručná ukázka každé předdefinované funkce. Detailnější popis každé funkce je přímo u její definice v souboru `lib/core.py`.

##### `+`
```lisp
(+ 1 10) ; -> 11
(+ 1.23 4.27) ; -> 5.5
(+ "hello " "world") ; -> "hello world"
```

##### `-`
```lisp
(- 123 23) ; -> 100
```

##### `*`
```lisp
(* 12 3) ; -> 36
(* 3 "hi") ; -> "hihihi"
```

##### `**`
```lisp
(** 8 2)
```

##### `/`
```lisp
(/ 26 3) ; -> 8.6666...
```

##### `//`
```lisp
(// 27 5) ; -> 5
```

##### `%`
```lisp
(% 14 5) ; -> 4
```

##### `=`
```lisp
(= 100 "100") ; -> false
```

##### `>=`
```lisp
(>= 5 6) ; -> false
```

##### `>`
```lisp
(> 5 3) ; -> true
```

##### `<=`
```lisp
(<= 4 5) ; -> true
```

##### `<`
```lisp
(< 5 -10) ; -> false
```

##### `append`
```lisp
(append 1 (list 0 2 3)) ; -> (0 2 3 1)
```

##### `assoc`
```lisp
(assoc {:a 10 :b 20} :c 30) ; -> {:a 10 :b 20 :c 30}
```

##### `dissoc`
```lisp
(dissoc {:a 10 :b 20} :a) ; -> {:b 20}
```

##### `concat`
```lisp
(concat [1 2] [3 4]) ; -> (1 2 3 4)
```

##### `contains?`
```lisp
(contains? :a {:b 20}) ; -> false
```

##### `count`
```lisp
(count [1 2 3]) ; -> 3
```

##### `empty?`
```lisp
(empty? [1]) ; -> false
```

##### `false?`
```lisp
(false? nil) ; -> false
```

##### `first`
```lisp
(first [1 2 3]) ; -> 1
(first ()) ; -> nil
```

##### `float?`
```lisp
(float? 8.2) ; -> true
```

##### `floor`
```lisp
(floor 4.49834) ; -> 4
```

##### `fn?`
```lisp
(fn? +) ; -> true
```

##### `get`
```lisp
(get :a {:a 10 :b 20}) ; -> 10
```

##### `hash-map`
```lisp
(hash-map :a 10 :b 20) ; -> {:a 10 :b 20}
```

##### `hash-map?`
```lisp
(hash-map? {}) ; -> true
```

##### `int?`
```lisp
(int? 44.44) ; -> false
```

##### `join`
```lisp
(join ", " [1 2 3 4]) ; -> "1, 2, 3, 4"
```

##### `keys`
```lisp
(keys {:a 10 :b 20 :c 30}) ; -> (:a :b :c)
```

##### `last`
```lisp
(last (list 1 2 3)) ; -> 3
```

##### `length`
```lisp
(length "123456") ; -> 6
```

##### `list`
```lisp
(list [1 2 3] 4 5) ; -> ([1 2 3] 4 5)
```

##### `list?`
```lisp
(list? [1 2 3]) ; -> false
```

##### `load-file`
```lisp
(load-file "examples/fibonacci_definition.plp")
(println (fast-fibonacci 100 1 0))
```

##### `nil?`
```lisp
(nil? nil) ; -> true
```

##### `not`
```lisp
(not false) ; -> true
(not 4) ; -> false
```

##### `nth`
```lisp
(nth 3 [1 2 3 4]) ; -> 4
```

##### `number?`
```lisp
(number? 4) ; -> true
(number? 4.44) ; -> true
```

##### `prepend`
```lisp
(prepend 0 [1 2 3]) ; -> (0 1 2 3)
```

##### `println`
Vypíše do konzole všechny argumenty, naformátované. `Stringy` vypisuje bez `""`. Vrací `nil`.
```lisp
(println 1 2 3 "hello world") ; -> vypíše: 1 2 3 hello world
```

##### `prn`
Vypíše do konzole všechny argumenty, naformátované. `Stringy` vypise s `""`. Vrací `nil`.
```lisp
(prn 1 2 3 "hello world") ; -> vypíše: 1 2 3 "hello world"
```

##### `pr-str`
Castne všechny argumenty na `String`, spojí se s mezerou, případně escapne potřebné znaky. Výsledný `String` vrací.
```lisp
(pr-str 1 2 3 "hello world") ; -> "1 2 3 \"hello world \""
```

##### `range`
```lisp
(range 1 11 2) ; -> (1 3 5 7 9)
```

##### `read-string`
Vezme PLP kód, naparsuje ho do PLP podoby. V PLP praxi něco jako `quote`. Využívá se k načtení kódu ze souborů.
```lisp
(read-string "(+ 1 2)")
```

##### `seq?`
```lisp
(seq? [1 2 3]) ; -> true
(seq? ()) ; -> true
(seq? {}) ; -> false
```

##### `slurp`
Otevře soubor, načte jeho obsah a vrátí ho jako `String`.
```lisp
(slurp "tests/slurp.txt") ; -> "hello world!"
```

##### `splice`
```lisp
(splice 1 -2 [1 2 3 4 5]) ; -> (2 3)
```

##### `split`
```lisp
(split ";" "hello;world;;") ; -> ("hello" "world" "" "")
```

##### `str`
Castne všechny argumenty na `String`, spojí se dohromady bez mezery. Vrací výsledek.
```lisp
(str 1 2 3 "hello world") ; -> "123hello world"
```

##### `string?`
```lisp
(string? 4) ; -> false
```

##### `symbol?`
```lisp
(symbol? +) ; -> false
(define a 10)
(symbol? a) ; -> true
(symbol? 4) ; -> false
```

##### `take`
```lisp
(take 3 (list 1 2 3 4 5 6)) ; -> (1 2 3)
```

##### `time`
```lisp
(time) ; -> čas
```

##### `time-ms`
```lisp
(time-ms) ; -> vrátí čas v nanosekundách od unixové epochy
```

##### `true?`
```lisp
(true? false) ; -> vrátí čas v milisekundách od unixové epochy
```

##### `type`
```lisp
(type 4) ; -> "Integer"
(type +) ; -> "function"
(type false) ; -> "Boolean"
```

##### `vals`
```lisp
(vals {:a 10 :b 20 :c 30}) ; -> (10 20 30)
```

##### `vec`
```lisp
(vec (list 1 2 3)) ; -> [1 2 3]
```

##### `vector`
```lisp
(vector 1 2 3) ; -> [1 2 3]
```