# Pebble

Pebble is a small interpreted programming language built from scratch in Python.

The project focuses on understanding the core components of a programming language, including **lexical analysis, parsing, abstract syntax trees, interpretation, variables, and runtime environments**.

Pebble is currently under active development, with new language features being added incrementally.

---

## Current Version

**V1.2 — Variable Language**

Pebble currently supports:

* Integers and floating-point numbers
* Addition, subtraction, multiplication, and division
* Operator precedence
* Parentheses and nested parentheses
* Unary `+` and `-` operators
* Variables and assignment
* Runtime environment for storing variables
* Basic lexical, syntax, and runtime error handling
* Interactive REPL

Example:

```text
pebble > x = 10
10

pebble > x + 5
15

pebble > x * 2
20
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
Environment
    ↓
Result
```

### Lexer

The lexer reads the source code and converts it into **tokens** such as numbers, identifiers, operators, and parentheses.

### Parser

The parser processes those tokens according to Pebble's syntax rules and builds an **Abstract Syntax Tree (AST)**.

The AST represents the structure of the code rather than the original text.

### Interpreter

The interpreter evaluates the AST and produces the result.

### Environment

The environment stores variables and their values during execution, allowing values to be reused in later expressions.

This structure gives Pebble a foundation for adding more programming-language features over time.

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
* Environment
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

You can then enter Pebble code:

```text
pebble > 10 + 5
15

pebble > 2 * (3 + 4)
14

pebble > x = 10
10

pebble > x + 5
15
```

To exit the REPL:

```text
pebble > bye()
```

---

## Version History

### V1 — Arithmetic Language

The first working version established Pebble's core language pipeline.

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

### V1.1 — Unary Operators

V1.1 extended the arithmetic system with **unary operators**.

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

### V1.2 — Variable Language

V1.2 introduces the foundation for storing and reusing values through **variables**.

Added:

* Identifiers
* Variable assignment
* Variable environment
* Variable-based expressions

Example:

```text
x = 10

x + 5
```

---

## Development

Pebble is still an evolving project. New language features will be added as development continues.

The language design and implementation may change as Pebble grows.

---

## License

This project is currently being developed as a personal educational project.