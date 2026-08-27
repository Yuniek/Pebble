# ##################################
# Importing Required Modules
# ##################################

import re

# ##################################
# Tokens
# ##################################

TOKEN_TYPES = [
    ('FLOAT',   r'\d+\.\d+'),
    ('INT',     r'\d+'),
    ('PLUS',    r'\+'),
    ('MINUS',   r'-'),
    ('MUL',     r'\*'),
    ('DIV',     r'/'),
    ('LPAREN',  r'\('),
    ('RPAREN',  r'\)'),
    ('WHITESPACE', r'\s+'),
]

class Token:
    def __init__(self, token_type, value:int|float|None, pos:dict[str, int]):
        self.type:str = token_type
        self.value:int|float|None = value
        self.pos = pos

    def __repr__(self)->str:
        if self.value is not None:return f'{self.type}:{self.value}'
        return f'{self.type}'


# ##################################
# Lexer to Generate Tokens
# ##################################

class Lexer:
    def __init__(self, text:str):
        self.text:str = text

    def tokenize(self) -> list[Token]:
        tokens = []

        pattern = '|'.join(f'(?P<{name}>{patern})' for name, patern in TOKEN_TYPES)

        position = 0

        for match in re.finditer(pattern, self.text):
            if match.start() != position:
                raise InvalidTokenError(position,match.start(),f"{self.text[position:match.start()]}")

            position = match.end()
            if match.lastgroup == 'WHITESPACE': continue
            token_type = match.lastgroup
            value = match.group()
            if token_type == 'FLOAT':
                value = float(value)
            elif token_type == 'INT':
                value = int(value)
            else:
                value = None
            tokens.append(Token(token_type, value, {'start':match.start(), 'end':match.end()}))

        if position != len(self.text):
            raise InvalidTokenError(
                position,
                len(self.text),
                self.text[position:]
            )

        tokens.append(Token("EOF", None, {'start':position, 'end':position}))
        return tokens

# ##################################
# Abstract Syntax Tree
# ##################################

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, number):
        self.number = number

    def __repr__(self) -> str:
        return f'NumberNode({self.number})'
    
class BinaryOperation(ASTNode):
    def __init__(self, left:ASTNode, op:str, right:ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f'({self.left} {self.op} {self.right})'

# ##################################
# Parser
# ##################################

class Parser:
    def __init__(self, tokens:list[Token]):
        self.tokens:list[Token] = tokens
        self.position:int = -1
        self.advance()

    def current_token(self) -> Token:
        return self.tokens[self.position]

    def advance(self):
        self.position += 1

    def parse(self):
        if len(self.tokens) < 2: return
        node = self.parse_expression()

        if self.current_token().type != 'EOF':
            raise InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                f"Unexpected token {self.current_token().type}"
            )

        return node
    
    def parse_factor(self)->ASTNode:
        current = self.current_token()
        if current.type in ('INT', 'FLOAT'):
            self.advance()
            return NumberNode(current.value)

        if current.type == 'LPAREN':
            self.advance()
            node = self.parse_expression()
            if self.current_token().type != 'RPAREN':
                raise InvalidSyntaxError(
                    self.current_token().pos['start'],
                    self.current_token().pos['end'],
                    "Expected ')'"
                )
            self.advance()
            return node

        raise InvalidSyntaxError(
            self.current_token().pos['start'],
            self.current_token().pos['end'],
            f"Expected a number or '(', got {current.type}"
        )
        
    def parse_term(self)->ASTNode:
        left = self.parse_factor()

        while self.current_token().type in ('MUL', 'DIV'):
            op = self.current_token()
            self.advance()
            right = self.parse_factor()

            left = BinaryOperation(left, op.type, right)
        
        return left

    def parse_expression(self)->ASTNode:
        left = self.parse_term()

        while self.current_token().type in ('PLUS', 'MINUS'):
            op = self.current_token()
            self.advance()
            right = self.parse_term()

            left = BinaryOperation(left, op.type, right)
        return left
 
# ##################################
# Interpreter
# ##################################

class Interpreter:
    def __init__(self, ast:ASTNode):
        self.ast = ast

    def evaluate(self, ast:ASTNode|None=None):
        if ast is None:
            return self.evaluate(self.ast)
        if isinstance(ast, NumberNode):
            return ast.number
        if isinstance(ast, BinaryOperation):
            left = self.evaluate(ast.left)            
            right = self.evaluate(ast.right)
            op = ast.op

            if op == "PLUS":
                return left + right
            elif op == "MINUS":
                return left - right
            elif op == "MUL":
                return left * right
            elif op == "DIV":
                if right == 0: raise PebbleRuntimeError(f"division by zero")
                return left / right
            else:
                raise PebbleRuntimeError(f"Unexpected Operator {op}")
                

# ##################################
# Errors
# ##################################

class PebbleError(Exception):
    def __init__(self, type_, pos_start, pos_end, detail):
        self.type       = type_
        self.pos_start   = pos_start
        self.pos_end     = pos_end
        self.detail     = detail
        super().__init__(self.detail)

class InvalidTokenError(PebbleError):
    def __init__(self, pos_start, pos_end, invalid_token):
            self.type       = "InvalidTokenError"
            self.detail     = f"Invalid token '{invalid_token}' at position {pos_start}"
            super().__init__(self.type, pos_start, pos_end, self.detail)

class InvalidSyntaxError(PebbleError):
    def __init__(self, pos_start, pos_end, detail):
            self.type       = "InvalidSyntaxError"
            self.detail     = f'{detail} at position {pos_start}'
            super().__init__(self.type, pos_start, pos_end, self.detail)

class PebbleRuntimeError(PebbleError):
    def __init__(self, detail):
            self.type       = "RuntimeError"
            self.detail     = detail
            super().__init__(self.type, None, None, self.detail)


# ##################################
# Run function to execute the code
# ##################################

def run(text:str):
    """
    text should be a pebble code.
    """
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    if ast is None:
        return None

    interpreter = Interpreter(ast)
    return interpreter.evaluate()
