# Todo

## Error handling

[ ] http://craftinginterpreters.com/evaluating-expressions.html#runtime-errors
[ ] http://craftinginterpreters.com/parsing-expressions.html#panic-mode-error-recovery
[ ] Simple stack trace
[ ] self.eat(TOKEN, "error string for better communication")
[ ] Show full text line of error
[ ] http://craftinginterpreters.com/functions.html#checking-arity

## Types

[ ] List
[ ] Dict

## Built-ins

[ ] to_int()
[ ] to_float()
[ ] to_string()
[ ] input()

## General

[ ] Proper return codes
[ ] AST visualizer
[ ] 1 <= x < 6, chained condition
[ ] 1_050_083: underscore for numbers ?
[ ] Separation between symbols and values
[ ] for loop / map ?
[ ] Helper function to build block statement lists (too much duplicated code)
[ ] Multi line REPL (rich repl?)
[ ] bool value of ""

## Done

[X] while
[X] Return statement
[X] FAIL-scope
[X] boolean
[X] if/then/else
[X] empty var declaration
[X] Basic REPL
[X] Partern matching all (\*)
[X] Integer
[X] Float
[X] String
[X] print
[X] input
[X] pattern matching

## Todo Notes

- Report as many distinct errors as there are. Aborting after the first error is easy to implement, but it’s annoying for users if every time they fix what they think is the one error in a file, a new one appears. They want to see them all.
- Minimize cascaded errors. Once a single error is found, the parser no longer really knows what’s going on. It tries to get itself back on track and keep going, but if it gets confused, it may report a slew of ghost errors that don’t indicate other real problems in the code. When the first error is fixed, those phantoms disappear, because they reflect only the parser’s own confusion.
