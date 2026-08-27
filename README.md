# Pebble

Pebble is a small programming language being built from scratch in Python.

The project is intentionally educational: the goal is not to make another Python clone, but to understand how programming languages work internally by implementing the language pipeline step by step.

## Objective

The long-term goal of Pebble is to become a simple, readable programming language that can be used to teach programming concepts to beginners.

The language is being designed around a few principles:

- Simple syntax that is easy for beginners to read.
- A real lexer, parser, AST, and interpreter instead of directly evaluating source text.
- Clear error messages with source positions.
- A codebase simple enough to study and understand from scratch.
- Enough features to eventually write useful programs with variables, conditions, loops, and functions.

---

## Current Version

### V1 — Arithmetic Language

Pebble currently supports arithmetic expressions and evaluates them using a tree-walk interpreter.

For example:

```text
pebble > 2 + 3 * 5
17

pebble > 2 * (3 + 5)
16

pebble > 10 / 2
5.0
```

It also correctly handles operator precedence:

```text
2 + 3 * 5
```

is interpreted as:

```text
2 + (3 * 5)
```

rather than:

```text
(2 + 3) * 5
```

---

## How Pebble Works

Pebble currently follows this pipeline:

```text
Source Code
     |
     v
   Lexer
     |
     v
   Tokens
     |
     v
   Parser
     |
     v
    AST
     |
     v
 Interpreter
     |
     v
   Result
```

### 1. Source Code

The user enters Pebble code:

```text
2 + 3 * (5 - 1)
```

### 2. Lexer

The lexer converts the source text into tokens:

```text
INT:2
PLUS
INT:3
MUL
LPAREN
INT:5
MINUS
INT:1
RPAREN
EOF
```

The lexer also stores the source position of every token so that errors can later point back to the original source.

### 3. Parser

The parser consumes the tokens and builds an Abstract Syntax Tree.

The expression:

```text
2 + 3 * 5
```

becomes conceptually:

```text
       PLUS
      /    \
     2      MUL
           /   \
          3     5
```

The parser uses:

```text
parse_expression()
        |
        v
   parse_term()
        |
        v
  parse_factor()
```

This structure is what gives multiplication and division higher precedence than addition and subtraction.

Parentheses are handled inside `parse_factor()`, allowing expressions to be nested recursively.

### 4. AST

The current AST contains:

- `ASTNode`
- `NumberNode`
- `BinaryOperation`

For example:

```text
2 + 3 * 5
```

produces a tree containing `NumberNode` and `BinaryOperation` instances.

### 5. Interpreter

The interpreter walks the AST recursively.

For:

```text
2 + 3 * 5
```

it effectively evaluates:

```text
3 * 5
  -> 15

2 + 15
  -> 17
```

This is a basic tree-walk interpreter.

---

## Current Syntax

### Numbers

Integers:

```text
10
875
21947
```

Floating-point numbers:

```text
3.14
10.5
```

### Operators

#### Addition

```text
2 + 3
```

#### Subtraction

```text
5 - 2
```

#### Multiplication

```text
4 * 5
```

#### Division

```text
10 / 2
```

### Parentheses

```text
2 * (3 + 5)
```

Nested parentheses are supported:

```text
((2 + 3) * 5)
```

### Operator precedence

Multiplication and division are evaluated before addition and subtraction.

```text
2 + 3 * 5
```

produces:

```text
17
```

while:

```text
(2 + 3) * 5
```

produces:

```text
25
```

---

## Error Handling

Pebble currently has a basic error hierarchy:

```text
PebbleError
├── InvalidTokenError
├── InvalidSyntaxError
└── PebbleRuntimeError
```

### Invalid token

The lexer rejects characters that are not part of the language:

```text
pebble > 5 @ 3
```

Result:

```text
InvalidTokenError: Invalid token '@' at position 2
```

### Invalid syntax

The parser detects malformed expressions such as:

```text
2 + * 5
```

or missing closing parentheses:

```text
2 * (3 + 5
```

### Runtime errors

The interpreter currently detects division by zero:

```text
10 / 0
```

and raises a runtime error instead of allowing the operation to silently produce an invalid result.

---

## Project Structure

Currently the project is intentionally small:

```text
Pebble/
├── pebble.py
├── README.md
└── shell.py
```

### `pebble.py`

Contains the language implementation:

```text
Token
Lexer
ASTNode
NumberNode
BinaryOperation
Parser
Interpreter
PebbleError
InvalidTokenError
InvalidSyntaxError
PebbleRuntimeError
run()
```

### `shell.py`

Contains the simple REPL:

```text
pebble >
```

It sends user input to `pebble.run()` and displays the result.

---

## Running Pebble

Make sure Python is installed.

From the project directory:

```bash
python shell.py
```

You should see:

```text
pebble >
```

Try:

```text
pebble > 2 + 3 * 5
17
```

To exit:

```text
pebble > bye()
```

---

## Development Roadmap
Pebble will be developed incrementally.

Future versions will expand the language beyond arithmetic expressions.

### Future: Unary Operators

Planned:

```text
-5
+10
-(2 + 3)
```

This will require extending the expression grammar and AST.

### Future: Variables

Planned syntax:

```text
x = 10
y = x + 5
y
```

This will introduce concepts such as:

- Variable nodes
- Assignment nodes
- Runtime environment
- Variable lookup
- Variable errors

### Future: Comparison & Boolean Values

Planned operators may include:

```text
==
!=
<
>
<=
>=
```

along with boolean values:

```text
true
false
```

### Future: Conditional Statements

Planned syntax may look similar to:

```text
if x > 10 {
    x + 1
}
```

This will introduce control flow and conditional AST nodes.

### Future: Loops

Planned features include loops such as:

```text
while x < 10 {
    x = x + 1
}
```

This will introduce:

- Loop AST nodes
- Repeated evaluation
- Control-flow handling
- Runtime state changes

### Future: Functions

Planned:

```text
fn add(a, b) {
    a + b
}

add(2, 3)
```

This will introduce:

- Function definitions
- Function calls
- Parameters
- Arguments
- Return values
- Function scopes

### Future: Strings

Planned support for values such as:

```text
"Hello"
"Pebble"
```

and eventually string operations.

### Future: Standard Library

Eventually Pebble may provide simple built-in functionality for teaching purposes, such as:

```text
print()
input()
```

and other beginner-friendly functionality.

### Future: Better Diagnostics

The current source-position system is intentionally simple.

Future versions may add:

- Line and column numbers
- Source snippets
- Error arrows/carets
- Better syntax explanations
- Runtime error locations
- AST source spans

For example:

```text
5 / 0
  ^

RuntimeError: division by zero
```

---

## Known Limitations

Pebble is still under active development.

Current limitations include:

### No unary operators

Expressions such as:

```text
-5
```

are not currently supported.

### No variables

Values cannot currently be stored in named variables.

### No statements

Pebble currently evaluates a single arithmetic expression rather than a sequence of statements.

### No functions

Functions, parameters, scopes, and return values do not exist yet.

### Runtime errors do not currently have source positions

The lexer stores positions on tokens, but AST nodes do not yet preserve their source spans.

Therefore an error such as:

```text
10 / 0
```

can report:

```text
RuntimeError: division by zero
```

but does not yet point directly at the `/` operator.

### Floating-point behavior

Floating-point numbers currently use Python's `float` type, so Pebble inherits normal floating-point behavior and limitations.

### Architecture is intentionally evolving

The current implementation is designed for learning and will change as the language gains more features.

---

## Design Philosophy

Pebble is being built from the bottom up rather than by translating Pebble syntax directly into Python.

The important stages are deliberately visible:

```text
Lexing
   ↓
Parsing
   ↓
AST construction
   ↓
Interpretation
```

As new language features are added, each feature should be understood through these stages.

For example, adding variables should not simply mean adding a Python dictionary somewhere. The feature should be understood as:

```text
source syntax
     ↓
tokens
     ↓
grammar
     ↓
AST
     ↓
runtime environment
     ↓
execution
```

This makes Pebble both a programming language project and a way to understand how interpreters and programming languages are constructed.

---

## Long-Term Goal

The long-term goal is for Pebble to become a small but complete interpreted programming language suitable for teaching programming fundamentals.

A future Pebble program should eventually be able to contain concepts such as:

```text
variables
conditions
loops
functions
data
expressions
```

while keeping the syntax and implementation approachable enough that a beginner can understand what is happening underneath.

Pebble is not trying to compete with Python, JavaScript, Rust, or other production languages.

Its purpose is to make the machinery behind a programming language understandable.

---

## Status

**V1 — Functional**

Pebble can currently tokenize, parse, construct an AST, and execute arithmetic expressions.

Future versions will expand Pebble from an arithmetic language into a general-purpose educational programming language.
