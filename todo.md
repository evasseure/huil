# Todo

[ ] AST visualizer
[ ] self.eat(TOKEN, "error string for better communication")
[ ] 1 <= x < 6, chained condition
[ ] 1_050_083: underscore for numbers ?
[ ] Separation between symbols and values
[ ] Show full text line of error
[ ] for loop / map ?
[ ] while ?
[ ] Helper function to build block statement lists (too much duplicated code)
[ ] to_int()
[ ] to_float()
[ ] to_string()
[ ] List
[ ] Dict
[ ] FAIL-scope
[ ] Simple stack trace
[ ] Multi line REPL (rich repl?)
[ ] http://craftinginterpreters.com/evaluating-expressions.html#runtime-errors
[ ] http://craftinginterpreters.com/parsing-expressions.html#panic-mode-error-recovery
[ ] bool value of ""
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
