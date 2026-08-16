from __future__ import annotations

from tokenizer import Token

# ============= NODES =============

# ----------- Structure -----------
class Program():
    def __init__(self, statements: list[Node]) -> None:
        self.statements = statements

class BodyTokens():
    def __init__(self, statements: list[Node]) -> None:
        self.statements = statements

class Node():
    def __init__(self) -> None:
        pass

class ExpressionNode(Node):
    def __init__(self) -> None:
        pass

# ---------- Declaration ----------
class VarDeclaration(Node):
    def __init__(self, type: str, name: str, val: ExpressionNode) -> None:
        self.type = type
        self.name = name
        self.val = val

class FunctionDeclaration(Node):
    def __init__(self, return_type: Token, name: Token, block: BodyTokens, params: list[Parameter] | None = None) -> None:
        self.return_type = return_type
        self.name = name
        self.params = params
        self.block = block

class Parameter(Node):
    def __init__(self, type: Token, name: Token) -> None:
        self.type = type
        self.name = name

# ---------- Statements ----------
class If(Node):
    def __init__(self, body: BodyTokens, next: If | None = None, condition: ExpressionNode | None = None) -> None:
        self.body = body
        self.next = next
        self.condition = condition

class While(Node):
    def __init__(self, body: BodyTokens, condition: ExpressionNode | None = None) -> None:
        self.condition = condition
        self.body = body

class For(Node):
    def __init__(self, loop_var: Token, iter: ExpressionNode, body: BodyTokens) -> None:
        self.loop_var = loop_var
        self.iter = iter
        self.body = body

class Return(Node):
    def __init__(self, val: ExpressionNode | None = None) -> None:
        self.val = val

class Stop(Node):
    def __init__(self) -> None:
        pass

class Continue(Node):
    def __init__(self) -> None:
        pass

class Get(Node):
    def __init__(self, mod: Token) -> None:
        self.mod = mod

# --------- Expressions ----------
class Literal(ExpressionNode):
    def __init__(self, val: Token) -> None:
        self.val = val

class Identifier(ExpressionNode):
    def __init__(self, name: Token) -> None:
        self.name = name

class Binary(ExpressionNode):
    def __init__(self, l: ExpressionNode, op: Token, r: ExpressionNode) -> None:
        self.l = l
        self.op = op
        self.r = r

class Unary(ExpressionNode):
    def __init__(self, op: Token, operand: ExpressionNode) -> None:
        self.op = op
        self.operand = operand

class AssignExpr(ExpressionNode):
    def __init__(self, target: Identifier | IndexExpr, val: ExpressionNode) -> None:
        self.target = target
        self.val = val

class CallExpr(ExpressionNode):
    def __init__(self, caller: Identifier, args: list[ExpressionNode]) -> None:
        self.caller = caller
        self.args = args

class IndexExpr(ExpressionNode):
    def __init__(self, indexee: Identifier, index: ExpressionNode) -> None:
        self.indexee = indexee
        self.index = index

class MemberAccess(ExpressionNode):
    def __init__(self, obj: Identifier, member: Identifier) -> None:
        self.obj = obj
        self.member = member

class CastExpr(ExpressionNode):
    def __init__(self, type: Token, castee: ExpressionNode) -> None:
        self.type = type
        self.castee = castee

def filter_token_list(tokens: list[Token]):
    iter_list = tokens.copy()
    for i, token in enumerate(iter_list):
        if token.token in ("TOKEN_SPACE", "TOKEN_NEWLINE", "TOKEN_COMMENT"):
            tokens.remove(token)
        
    for i, token in enumerate(tokens):
        if token.token in ("TOKEN_MALFORMEDNUM", "TOKEN_UNTERMSTR", "TOKEN_CHARTOOLONGORUNTERM"):
            match token.token:
                case "TOKEN_MALFORMEDNUM":        raise errors.MalformedNumber("Number malformed.")
                case "TOKEN_UNTERMSTR":           raise errors.UnterminatedString("String unterminated.")
                case "TOKEN_CHARTOOLONGORUNTERM": raise errors.CharacterTooLong("Character type too long.")
                case _:                           raise Exception("Unknown error occured.")
    
    return tokens

def parse_var_dec(tokens, i):
    token = tokens[i]

    while token.token != "TOKEN_SEMI":
        token = tokens[i]

        if i + 1 >= len(tokens): next_char_end = True
        else:                    next_char_end = False

        match token.token:
            case "TOKEN_INT":   type = "Integer"
            case "TOKEN_CHAR":  type = "Character"
            case "TOKEN_STR":   type = "String"
            case "TOKEN_BOOL":  type = "Boolean"
            case "TOKEN_FLOAT": type = "Floating_Point"
            case "TOKEN_DICT":  type = "Dictionary"
            case "TOKEN_INFER": type = "Inferred_Var"
            case "TOKEN_VOID":  raise errors.TypeDeclarationError("Variable declaration cannot be of type `void`.")
            case "TOKEN_VARID": identifier = token.value
            case "TOKEN_ASSIGN": 
                if not next_char_end:
                    if tokens[i + 1].token in ["TOKEN_NUMBER", "TOKEN_STRING"]:
                        value = Literal(tokens[i + 1].value)
                    else:
                        raise errors.DeclarationError("Value must be of class `Literal`.")
                else:
                    raise errors.DeclarationError("Variable assigns with `=` but no value follows.")
                
        i += 1

    new_index = i

    VarDeclaration_instance = VarDeclaration(type, identifier, value)

    return (VarDeclaration_instance, new_index)