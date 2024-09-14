### Python List Processing (PLP)
#### Definice
**Python List Processing** (dále jako **PLP**) je pokus o vytvoření interpretu vlastního dialektu LISPu.

Výsledkem je program, který je schopný pracovat s předem zadefinovanou syntaxí, zpracovat jednotlivé výrazy, ukládat proměnné, definovat funkce, ...

#### Struktura
Projekt obsahuje 3 složky:
- `examples` obsahuje příklady jednoduchých programů, které je PLP schopné zpracovat,
- `lib` obsahuje soubory zdrojového kódu,
- `tests` obsahuje testovací data.

A spustitelné soubory `main.py` a `test.py` v hlavním adresáři.

#### Jak to funguje?
Program načte kód zapsaný v PLP syntaxi, tento text rozdělení na jednotlivé tokeny, které dále podle určitých pravidel naparsuje na čísla, stringy, pole, booleany atd. Z nich vytvořít abstraktní syntatický strom (AST), který následně projde a vykoná jednotlivé operace na daných operandech.

Vzhledem k LISPovské povaze je syntaxe zpracovávána řádku po řádce, resp. výraz poo výrazu. O syntaxi dále v textu.

##### `main.py`
Obsahuje hlavní logiku programu. Spustí hlavní funkci, která buď uvedene program do konzolové aplikace, ve které je možné spouštět jednotlivé PLP výrazy, nebo spustí předané `.plp` soubory.

##### `test.py`
Soubor, ve kterém je sepsán jednoduchý testovací systém, který spustí všechny testovací data ze složky `tests`, vypíše jednotlivé testy a shrnutí celkového testování.

##### `lib/rep.py`
Zahrnuje logiku konzolového prostředí, ve kterém dochází ke spouštění jednotlivých PLP výrazů. Dále jsou zde globálně zadefinované nějaké funkce v samotné PLP syntaxi jako proof-of-concept.

##### `lib/eval.py`
Obsahuje klíčovou funkci `EVAL`, která zpracovává abstraktní syntaktický strom daného PLP výrazu. Tato funkce je asi z celého projektu ta nejdůležitější, a tím pádem nejsložitější (ve skutečnosti je úplně jednoduchá). Než ji složitě popisovat, stačí porozumět PLP syntaxi a pak při jejím čtení vše do sebe zapadne.

##### `lib/reader.py`
Zde je sepsána logika zpracování textové syntaxe do abstraktního syntaktického stromu, který je dále předán již zmíněné `EVAL` funkci.

##### `lib/env.py`
Obsahuje třídu prostředí, ve kterém dochází ke globálním/lokálním definicím a jejich referenci při zpracování AST.

##### `lib/core.py`
Soubor s definicemi základních PLP funkcí pro manipulaci s daty.

##### `lib/exceptions.py`
Definice vlastních chybových tříd a formátování jejich specifických chybových hlášek.

##### `lib/helper.py`
Pár jednoduchých funkcí, které jsou využívané na různých místech ryze pro práci s AST.

##### `lib/plp_types.py`
Zde jsou zadefinované všechny třídy PLP typů, které slouží k bližšímu upřesnění při práci s AST a zároveň pro typovou anotaci Pythonovského kódu.

##### `lib/printer.py`
Obsahuje funkci zadávající, jak vypsat jednotlivé PLP typy. Což by šlo jednoduše vyřešit přes Pythonovskou funkci `print` a pro každou třídu PLP typu zadefinovat funkci `__str__`. S tímto přístupem jsem začal, ale následně jsem se rozhodl jej pozměnit na ten stávající, neboť mi příšlo, že je více flexibilní pro program tohoto typu.

#### Testování
Nežli testovat samotné funkce interpretu, jsou testované pouze PLP výrazy, které jsou následně prohnány samotným interpretem, takže jistým způsobem dochází k testování i samotného kódu. Zároveň celý Python kód je otypovaný, což (snad) předejde některým možných chybám.

Testování je ale dlouhodobě neudržitelné. Chtělo by to lepší systém, ideálně mít testy zadefinované hned u definic jednotlivých funkcí, což by nutilo k tomu psát testy hned u definice funkce, a bylo by to více přehledné a snazší dané testy vyhledat.

Při spuštění testování se ukáže pár testů, které selžou. To je úmyslné, neboť se jedná o chování, které není tak časté, ale je nějakým způsobem zahrnuto v tomto interpretu a u kterého nevím, jaká je ideální implementace. Proto místo nějakého řešení, jsem nechal tyto problémy otevřené diskusi – jedná se o primitivní parsovací chyby, tedy nejde ryze o lenost z mé strany se tím zabývat. (Kdybych býval smazal těch pár testů, nikoho by ani nenapadlo, že je něco špatně.)

Kdyby se mohlo testování někde dodělat, bylo by to určitě v té parsovací části. Při dokončování projektu jsem objevil pár výrazů, jejichž část parser vyignoruje, místo čehož by měl ideálně zobrazit chybovou hlášku. Jedná se o výrazy typu `(+ 2 3))))))`, kde jsou přebytečné závorky na konci (to stejné se týká komentářů na konci výrazu), které parser ignoruje a výraz úspěšně zpracuje a dostaneme z něj „správný“ AST: `[Symbol("+"), Integer(2), Integer(3)]`.

##### Spuštění testů
Testy jsou uložený ve složce `tests`.
Všechny testy lze spustit naráz příkazem `python3 test.py`, který do konzole vypíše jednotlivé testy a shrnutí jejich výsledků.
Existuje rozšíření příkazu: `python3 test.py --show-failed`, kdy se na konci vypíšou všechny testy, které selhaly.
Dále lze spustit pouze jednotlivý test podle názvu jeho souboru. A to pomocí příkazu `python3 test.py "nazev-testu-ve-slozce.plptest"`. (V tomto případě nelze použít rozšíření `--show-failed`.)

##### Syntax testovacích dat

Pro potřeby testování jsem vytvořil vlastní jednoduchou testovací syntax pro zapisování testovacích dat.

Každý výraz k otestování je na samostatné řádce. Další řádka musí začínat středníkem (`;`) a ihned po něm následuje očekávaná odpověď interpretu. Nezačíná-li následující řádka středníkem, je výraz pouze spuštěn – může sloužit k zadefinování proměnné, která se může využít v dalším testu. Je-li po středníku zapsán výraz `err!`, očekává se, že vykonání výrazu selže.

Dále lze využít komentářů, které jsou označený dvěma po sobě jdoucímí středníky (`;;`). Komentáře jsou vypsány do konzole během testování. Slouží k upřesnění následujícíh testů.

Prázdné rádky jsou ignorovány.

##### Ukázka využití testovací syntaxe
```
;; Testování definovaní proměnných
(define world "world")
;"world"

(define hello world)
;"world"

hello
;"world"
```

#### Omezení
Interpet je samozřejmě omezen zadefinovanou funkcionalitou, která není tak obsáhla, neboť projekt byl spíš proof-of-concept.

Všechno zadefinované funguje, jak má, až na hlídání chyb. Program je samozřejmě schopen (téměř[^1]) vždy zachytit chybové chování a ukončí se s chybovou hláskou. Chybové hlášky jsou vesměs vždy správné ohlídané a předají, co špatného se stalo.

Systém na záchyt chyb však není tak rozsáhly, aby byl schopen ukázat celý výraz, pozici chyby a tak, jak je tomu zvyku u většiny programovacích jazyků. Dalším nedostatkem je zavolání nějaké PLP funkce, která dostane argumenty jiných typů, než očekává. Vyřešení tohoto problému je až moc složité vzhledem k velikosti tohoto projektu. (Avšak jako proof-of-concept je zadefinováno pár funkcí – např. `+`, `-` –, u kterých se kontrolují i typy a počet argumentů. Jak již bylo řečeno, tyto definice jsou ale moc dlouhé a nepřehledné, a proto jsem se rozhodl zbytek si zbytek definic funkcí usnadnit.)

Chyby vždy pochází z nesprávně užití PLP syntaxe. Tedy bude-li korektně zapsaná, žádné chyby se nevyskytnou. To se projevuje převážně i do testování různých výrazů – nežli vychytávat chyby, zaměřil jsem se více na to, že je-li výraz správně zapsán, dostaneme správný výsledek.

[^1]: Až na drobné parsovací chyby, které ryze nastavájí pouze na konci daného výrazu a žádným výrazným způsobem nezasahují do správného chování interpretu.

#### Možná vylepšení
Zde jsou uvedené různé funkcionality, které jiné programovací jazyky nabízí a kterými by se PLP dalo rozšířit:
- další varianty loopů (`for () {}`, `for () in () {}`, ...),
- LISPovské `quasiquote`, `unquote`, `def-macro`, ...,
- `and`, `or`, ... logical clauses,
- lepší type-system,
- rozšířená práce se soubory,
- [lazy sequences](ttps://clojuredocs.org/clojure.core/lazy-seq),
- garbage collector,
- multi-threading,
- namespaces,

a samozřejmě již zmíněné, lepší chybové hlášky.

#### Požadavky a ovládání
##### Požadavky
PLP vyžaduje alespoň (myslím) `Python 3.10+`, ale program byl testován pouze na verzi `3.12.6`. Nevyužívá žádné externí knihovny kromě těch v základní výbavě.

##### Spuštění
PLP má 2 režimy:
- načte soubor, přečte jej, zpracuje a případně vypíše potřebné věci do konzole,
- nebo se načte do tzv. `REPL` režimu `(read-eval-print-loop)`, ve kterém lze krok po kroku vykonávat příkazy.

`REPL` režim se spustí pomocí
```
python3 main.py
```
čímž se otevře prostředí, ve kterém lze dělat například
```
plp> (define hello "world")
"world"
plp> (split "" hello)
("w" "o" "r" "l" "d")
plp> (do ((define ! (fn (n) (if (= n 1) 1 (* n (! (- n 1)))))) 20))
3628800
```
Nebo příkazem
```
python3 main.py "path/to/file.plp" "path/to/another/file.plp" ...
```
lze spustit několik souborů naráz. Můžete zkusit spustit předpřipravený soubor
`python3 main.py examples/fibonacci.plp`:
```
calculating 22-th fibonacci number
[fast-fibonacci] 0.000337s
[slow-fibonacci] 0.59333s

calculating 100000-th fibonacci number
[fast-fibonacci] 1.343841s
[slow-fibonacci] ... way too slow

try it yourself by running (load-file 'examples/fibonacci_definition.plp')
and then use it like (fast-fibonacci N 1 0)
```
Cesta k souborům je relativní k umistění souboru `main.py`. Soubory se spouští jeden po druhém a všechny pracují ve stejném prostředí, tedy nově zadefinované výrazy se přenášejí dál a záleží na jejich pořadí.

##### Ukázky
Ve složce `examples` je sepsáno pár jednoduchých programů v PLP syntaxi, které je možné spustit a otestovat jimi tento interpret.

#### Syntax

Zadefinovaná PLP syntax je vysvětlená [zde](SYNTAX.md).

#### Osobnostní rozvoj
Toto zadaní jsem si vybral z důvodu, že jsem dosud neměl žádné zkušenosti s LISPem ani s interpretováním nějakého jiného jazyka. A musím říct, že jsem si toho hodně odnesl. Dokonce musím přiznat, že zpracování projektu ve mně vzbudilo další zájem o tuto oblast programování. Ale celý proces nebyl vůbec příjemný...

Osobně jsem zastáncem toho, že kód má mluvit za člověka, což mi u Pythonu přijde nereálné, neboť je to dynamicky typovaný jazyk, který je z velké části objektově orientovaný, ale vlastně to není ani znát.

Díky novějším verzím Pythonu je možné adekvátně anotovat typy, což velmi přispívá k dobré komunikaci, ale vůbec nic to neznamená. Celý konečný projekt mi přijde hrozně křehký, jako kdyby ho jeden špatně zapsaný znak mohl rozbít. Mnohokrát se mi stalo, že jsem udělal chybu, špatně něco anotoval, type-checkeru to vůbec nevadilo, program se spustil a choval se nepředvídatelně. Kdybych pracoval na větším projektu, asi bych se z toho časem zhroutil. Tím se jen potvrdila moje idiosynkrasie vůči Pythonu, která také vychází z absence závorkování (což řešení například preprocessor Bython), důrazu na globální funkce i přes OOP vlastnosti Pythonu, zvláštních scopů proměnných, ... *Možná to však vychází ryze jen z mé nedostatečné znalosti Pythonu?* Tím neříkám, že Python je špatný jazyk, jen že já nejsem, a už asi nikdy nebudu jeho fanouškem.

I přes to mi ale Python přinesl něco dobrého. Díky němu jsem vlastně objevil krásu LISPu. Nevím zcela proč, ale jeho závorková syntaxe mi velmi imponuje. A rád bych jej v blízké době prozkoumal víc. Líbí se mi, že LISP ví přesně, čím je, a na nic si nehraje narozdíl od Pythonu, který je v dnešní době takovým univerzálním řešením na všechno možné, i když existuje jazyk, který by pro daný účel byl mnohem lepší.