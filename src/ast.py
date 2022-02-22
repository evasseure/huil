from dataclasses import dataclass
from tokenize import Token
from typing import Any, List


@dataclass
class ASTNode:
    token: Token


@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    right: ASTNode


@dataclass
class BooleanNode(ASTNode):
    value: bool


@dataclass
class UnaryOpNode(ASTNode):
    value: ASTNode


@dataclass
class NumNode(ASTNode):
    value: int or float


@dataclass
class StringNode(ASTNode):
    value: str


@dataclass
class NilNode(ASTNode):
    ...


@dataclass
class VariableNode(ASTNode):
    id: str


@dataclass
class MatchNode(ASTNode):
    factor: ASTNode
    matches: List[List[ASTNode]]


@dataclass
class FunctionNode(ASTNode):
    id: str
    arguments: List[str]
    statements: "StatementListNode"


@dataclass
class IfThenElseNode(ASTNode):
    conditions: List[ASTNode]
    truthy_statements: List["StatementListNode"]
    else_statements: "StatementListNode"


@dataclass
class FunctionCallNode(ASTNode):
    id: str
    arguments: List[Any]


@dataclass
class AssignmentNode(ASTNode):
    id: str
    value: Any


@dataclass
class DeclarationNode(ASTNode):
    id: str
    value: Any


@dataclass
class StatementListNode(ASTNode):
    statements: List[ASTNode]
