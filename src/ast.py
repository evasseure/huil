from dataclasses import dataclass
from tokenize import Token


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
