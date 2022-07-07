![Olive oil image](./huil.png)

# Huil

**H**ighly **U**noptimized **I**nterpreted **L**anguage is a **general purpose language**.  
I just wanted to play a bit with programming languages, so this is simply a learning project. Don't expect clean code, or even a functional language. There are no tests, and I didn't try to optimize anything.

## Usage

To interpret a file:  
`poetry run python main.py -f examples/test`

To use the REPL (does not work well):  
`poetry run python main.py`

## Examples

Variables and functions:

```
fn add(a, b):
    return a + b

fn mult(c, d):
    let res = c * d
    return res

let var1 = 2
let var2 = 4
let res = add(var1, mult(var2, 2))
print(res)
```

While loop:

```
let x = 0
while x != 6:
    print(x)
    x = x + 1
```

Variable scope:

```
let a = 5
print(a) // 5

fn test(a):
    print(a) // 2

test(2)
print(a) // 5
```

Pattern matching:

```
print("Type a number to translate (0 -> 9):")
let num = input("-> ")
let letter = match num:
    | 0 -> "zero"
    | 1 -> "one"
    | 2 -> "two"
    | 3 -> "three"
    | 4 -> "four"
    | 5 -> "five"
    | 6 -> "six"
    | 7 -> "seven"
    | 8 -> "height"
    | 9 -> "nine"
    | * -> "I don't know sorry"
```

## Grammar

```
statements: statement+

statement:
    | compound_stmt
    | simple_stmts

simple_stmts: simple_stmt NEWLINE

simple_stmt:
    | declaration
    | assignment
    | expression
    | return_stmt

compound_stmt:
    | function_def
    | if_stmt
    | while_stmt
    | match_stmt

declaration: 'let' ID ['=' expression]

assignment: ID '=' expression

function_def: 'fn' ID '(' [ID (',' | ID)*] ')' ':' block

if_stmt:
    | 'if' expression ':' block elif_stmt
    | 'if' expression ':' block [else_stmt]

elif_stmt:
    | 'elif' expression ':' block elif_stmt
    | 'elif' expression ':' block [else_stmt]

else_stmt: 'else' ':' block

while_stmt: 'while' expression: block

match_stmt: 'match' expression ':' NEWLINE INDENT (match)+ DEDENT

match: '|' (expression | '*') '->' expression

block: NEWLINE INDENT statements DEDENT

return_stmt: `return` expression

expression:
    | term
    | expression '+' term
    | expression '-' term
    | expression '>' term
    | expression '>=' term
    | expression '<' term
    | expression '<=' term
    | expression '==' term
    | '!' term // NOT IMPLEMENTED YET
    | expression 'or' term
    | expression 'and' term

term:
    | factor
    | term '*' factor
    | term '/' factor
    | term '//' factor
    | term '%' factor

factor:
    | primary
    | '+' factor
    | '-' factor

primary:
    | atom
    | ID '(' [expression (',' | expression)*] ')'

atom:
    | ID
    | INTEGER
    | FLOAT
    | STRING
    | 'true'
    | 'false'
    | None // NOT IMPLEMENTED YET
    | '(' expression ')'
```

## Links

My main resource is: http://craftinginterpreters.com/, it's simply an amazing book.  
Some other resources I think I used:

- https://thesephist.com/posts/pl/
- https://norvig.com/lispy.html
- https://softwareengineering.stackexchange.com/questions/254074/how-exactly-is-an-abstract-syntax-tree-created
- https://medium.com/young-coder/how-i-wrote-a-lexer-39f4f79d2980
- https://astexplorer.net/#/gist/e675b0068a8b74098c213b8065d7583c/dac289f77e481e68fdff052392aa789ee05d4e78
- https://github.com/dabeaz/ply
- https://github.com/lark-parser/lark/
