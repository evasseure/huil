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
class UnaryOpNode(ASTNode):
    value: ASTNode


@dataclass
class NumNode(ASTNode):
    value: int or float


@dataclass
class VariableNode(ASTNode):
    id: str


@dataclass
class FunctionNode(ASTNode):
    id: str
    arguments: List[str]
    statements: "StatementListNode"


@dataclass
class FunctionCallNode(ASTNode):
    id: str
    arguments: List[Any]


@dataclass
class AssignmentNode(ASTNode):
    id: str
    value: Any


@dataclass
class StatementListNode(ASTNode):
    statements: List[ASTNode]
