# Pebble

Pebble is a small interpreted programming language built from scratch in Python.

The project is focused on understanding the fundamental components of a programming language, including lexical analysis, parsing, abstract syntax trees, and interpretation.

Pebble is currently under active development, with new language features being added incrementally.

---

## Current Version

**V1.1 — Unary Operators**

Pebble currently supports:

- Integers and floating-point numbers
- Addition, subtraction, multiplication, and division
- Operator precedence
- Parentheses and nested parentheses
- Unary `+` and `-` operators
- Basic lexical, syntax, and runtime error handling

Example:

```text
pebble > 2 + 3 * 4
14

pebble > -(2 + 3)
-5

pebble > 5 * -3
-15
```
---
## How Pebble Works

Pebble processes code through several stages:

```text
Source Code
    ↓
Lexer
    ↓
Tokens
    ↓
Parser
    ↓
AST
    ↓
Interpreter
    ↓
Result
```

### Lexer

The lexer reads the source code and converts it into **tokens** such as numbers, operators, and parentheses.

### Parser

The parser processes those tokens according to Pebble's syntax rules and builds an **Abstract Syntax Tree (AST)**.

The AST represents the structure of the expression rather than the original text.

### Interpreter

The interpreter evaluates the AST and produces the final result.

This architecture allows Pebble to grow into a larger programming language without directly executing the source code as Python.

---

## Project Structure

```text
Pebble/
├── pebble.py
├── README.md
└── shell.py
```

### `pebble.py`

Contains the core implementation of the Pebble language:

* Lexer
* Parser
* AST nodes
* Interpreter
* Error handling
* `run()` function

### `shell.py`

Provides a simple **REPL (Read-Eval-Print Loop)** for interacting with Pebble from the terminal.

---

## How to Use

### Requirements

* Python 3.10 or newer

### Run Pebble

Open a terminal in the project directory and run:

```bash
python shell.py
```

You will see:

```text
pebble >
```

You can then enter Pebble expressions:

```text
pebble > 10 + 5
15

pebble > 2 * (3 + 4)
14

pebble > -10 / 2
-5.0
```

To exit the REPL:

```text
pebble > bye()
```

---

## Version History

### V1 — Arithmetic Language

The first working version of Pebble established the core language pipeline.

Introduced:

* Integer and floating-point numbers
* Basic arithmetic operators
* Operator precedence
* Parentheses
* Lexer
* Recursive-descent parser
* Abstract Syntax Tree
* Tree-walk interpreter
* Basic error handling
* Interactive REPL

This version established the foundation on which later versions are being built.

### V1.1 — Unary Operators

V1.1 extends the arithmetic system with **unary operators**.

Added:

* Unary `+`
* Unary `-`
* Chained unary operators
* Unary operators with parentheses
* Unary operators combined with binary expressions
* Improved REPL error handling

Examples:

```text
-5
+5
--5
-(2 + 3)
5 * -3
2 + -3 * 4
```

---

## Development

Pebble is still an evolving project.

Future versions will gradually introduce additional programming-language features such as variables, boolean values, control flow, functions, strings, and other language constructs.

The language design and implementation may change as the project develops.

---

## License

This project is currently being developed as a personal educational project.