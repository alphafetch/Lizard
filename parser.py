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
    def __init__(self, type: Token, name: Token, val: ExpressionNode) -> None:
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
    def __init__(self, body: BodyTokens, next: If | None = None, condition: list[Token] | None = None) -> None:
        self.body = body
        self.next = next
        self.condition = condition

class While(Node):
    def __init__(self, body: BodyTokens, condition: list[Token] | None = None) -> None:
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