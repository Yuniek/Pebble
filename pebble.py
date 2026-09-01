# ##################################
# Importing Required Modules
# ##################################

import re

# ##################################
# Tokens
# ##################################

TOKEN_TYPES = [
    ('KEYWORD',          r'\b(true|false)\b'),
    ('FLOAT',            r'\d+\.\d+'),
    ('INT',              r'\d+'),
    ('GREATER_OR_EQUAL', r'>='),
    ('LESSER_OR_EQUAL',  r'<='),
    ('GREATER',          r'>'),
    ('LESSER',           r'<'),
    ('EQUALITY',         r'=='),
    ('NOT_EQUAL',        r'!='),
    ('AND',              r'and'),
    ('OR',               r'or'),
    ('NOT',              r'not'),
    ('EQUAL',            r'='),
    ('PLUS',             r'\+'),
    ('MINUS',            r'-'),
    ('MUL',              r'\*'),
    ('DIV',              r'/'),
    ('LPAREN',           r'\('),
    ('RPAREN',           r'\)'),
    ('STRING',           r'\".*?\"'),
    ('IDENTIFIER',       r'[A-Za-z_][A-Za-z0-9_]*'),
    ('WHITESPACE',       r'\s+'),
]

class Token:
    def __init__(self, token_type, value:int|float|str|None, pos:dict[str, int]):
        self.type:str = token_type
        self.value:int|float|str|None = value
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

        pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)

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
            elif token_type == 'STRING':
                value = value[1:-1]
            elif token_type == 'IDENTIFIER':
                value = value
            elif token_type == 'KEYWORD':
                value = value
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
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f'NumberNode({self.value})'

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f'BooleanNode({self.value})'

class StringNode(ASTNode):
    def __init__(self, value):
            self.value = value

    def __repr__(self) -> str:
        return f'StringNode({self.value})'

class IdentifierNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"Identifier({self.value})"

class UnaryOperation(ASTNode):
    def __init__(self, op:str, operand:ASTNode):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f'({self.op} {self.operand})'

class BinaryOperation(ASTNode):
    def __init__(self, left:ASTNode, op:str, right:ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f'({self.left} {self.op} {self.right})'

class AssignmentNode(ASTNode):
    def __init__(self, identifier:IdentifierNode, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"{self.identifier} = {self.expression}"

class BooleanOperation(ASTNode):
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
        if self.current_token().type == 'IDENTIFIER' and self.tokens[self.position+1].type == 'EQUAL':
            node = self.parse_identifier()
        else:
            node = self.parse_or()

        if self.current_token().type != 'EOF':
            raise InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                f"Unexpected token {self.current_token().type}"
            )

        return node

    def parse_identifier(self)->ASTNode:
        identifier = IdentifierNode(self.current_token().value)
        self.advance()
        if self.current_token().type != "EQUAL":
            raise InvalidSyntaxError(
                self.current_token().pos['start'],
                self.current_token().pos['end'],
                f"Expected '=' after identifier token but got {self.current_token().type}"
            )
        self.advance()
        expression = self.parse_or()
        return AssignmentNode(identifier, expression)

    def parse_unary(self)->ASTNode:
        op = self.current_token().type
        self.advance()
        operand = self.parse_factor()
        return UnaryOperation(op, operand)
    
    def parse_factor(self)->ASTNode:
        current = self.current_token()
        if current.type in ('INT', 'FLOAT'):
            self.advance()
            return NumberNode(current.value)
        
        if current.type == 'KEYWORD' and current.value in ('true', 'false'):
            self.advance()
            return BooleanNode(True) if current.value == 'true' else BooleanNode(False)

        elif current.type == 'LPAREN':
            self.advance()
            node = self.parse_or()
            if self.current_token().type != 'RPAREN':
                raise InvalidSyntaxError(
                    self.current_token().pos['start'],
                    self.current_token().pos['end'],
                    "Expected ')'"
                )
            self.advance()
            return node

        elif current.type in ('PLUS', 'MINUS', 'NOT'):
            return self.parse_unary()

        elif current.type == 'IDENTIFIER':
            self.advance()
            return IdentifierNode(current.value)

        raise InvalidSyntaxError(
            self.current_token().pos['start'],
            self.current_token().pos['end'],
            f"Expected a number, '(', '+', or '-', got {current.type}"
        )

    def parse_term(self)->ASTNode:
        left = self.parse_factor()

        while self.current_token().type in ('MUL', 'DIV'):
            op = self.current_token().type
            self.advance()
            right = self.parse_factor()

            left = BinaryOperation(left, op, right)
        
        return left

    def parse_expression(self)->ASTNode:
        left = self.parse_term()

        while self.current_token().type in ('PLUS', 'MINUS'):
            op = self.current_token().type
            self.advance()
            right = self.parse_term()

            left = BinaryOperation(left, op, right)
        return left

    def parse_comparison(self)->ASTNode:
        left = self.parse_expression()

        while self.current_token().type in ("GREATER_OR_EQUAL", "LESSER_OR_EQUAL", "GREATER", "LESSER", "EQUALITY", "NOT_EQUAL"):
            op = self.current_token().type
            self.advance()
            right = self.parse_expression()

            left = BooleanOperation(left, op, right)
        return left

    def parse_and(self)->ASTNode:
        left = self.parse_comparison()

        while self.current_token().type == "AND":
            op = self.current_token().type
            self.advance()
            right = self.parse_comparison()

            left = BooleanOperation(left, op, right)
        return left

    def parse_or(self)->ASTNode:
        left = self.parse_and()

        while self.current_token().type == "OR":
            op = self.current_token().type
            self.advance()
            right = self.parse_and()

            left = BooleanOperation(left, op, right)
        return left

# ##################################
# Interpreter
# ##################################

class Environment:
    def __init__(self):
        self.environment = {}
    def setVariable(self, var_name:str, var_value:str|int|float|None):
        self.environment[var_name] = var_value
    def getVariable(self, var_name:str):
        if var_name not in self.environment:
            raise PebbleRuntimeError(f"Unknown variable {var_name}")
        return self.environment[var_name]

class Interpreter:
    def __init__(self, ast:ASTNode, env:Environment):
        self.ast = ast
        self.env = env

    def evaluate(self, ast:ASTNode|None=None):
        if ast is None:
            return self.evaluate(self.ast)
        if isinstance(ast, NumberNode):
            return ast.value
        if isinstance(ast, IdentifierNode):
            return self.env.getVariable(ast.value)
        if isinstance(ast, AssignmentNode):
                    identifier = ast.identifier.value
                    expression = self.evaluate(ast.expression)
                    self.env.setVariable(identifier, expression)
                    return None
        if isinstance(ast, BooleanNode):
                    return ast.value
        if isinstance(ast, UnaryOperation):
            if ast.op == 'PLUS':
                return self.evaluate(ast.operand)
            if ast.op == 'MINUS':
                return self.evaluate(ast.operand) * -1
            if ast.op == 'NOT':
                return not bool(self.evaluate(ast.operand))
            else:
                raise PebbleRuntimeError(f"Unexpected Unary Operator {ast.op}")
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
                raise PebbleRuntimeError(f"Unexpected Binary Operator {op}")
        if isinstance(ast, BooleanOperation):
            left = self.evaluate(ast.left)
            right = self.evaluate(ast.right)
            op = ast.op

            match op:
                case 'OR':
                    return bool(left) or bool(right)
                case 'AND':
                    return bool(left) and bool(right)
                case 'NOT_EQUAL':
                    return left != right
                case 'EQUALITY':
                    return left == right
                case 'LESSER':
                    return left < right
                case 'GREATER':
                    return left > right
                case 'LESSER_OR_EQUAL':
                    return left <= right
                case 'GREATER_OR_EQUAL':
                    return left >= right
                case _:
                    raise PebbleRuntimeError(f"Unexpected Boolean Operator {op}")

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

def run(text:str, env):
    """
    text should be a pebble code.
    """
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)

    if ast is None:
        return None

    interpreter = Interpreter(ast, env)
    return interpreter.evaluate()
