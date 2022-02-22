from src.token import *


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.unhandled_visit)
        return visitor(node)

    def unhandled_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.global_scope = {}

    def visit_BinaryOpNode(self, node):
        if node.token.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.token.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.token.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.token.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.token.type == MOD:
            return self.visit(node.left) % self.visit(node.right)

    def visit_UnaryOpNode(self, node):
        if node.token.type == PLUS:
            return self.visit(node.value)
        elif node.token.type == MINUS:
            return -self.visit(node.value)

    def visit_NumNode(self, node):
        return node.value

    def visit_AssignmentNode(self, node):
        self.global_scope[node.id.value] = self.visit(node.value)

    def visit_VariableNode(self, node):
        if self.global_scope.get(node.id) == None:
            raise NameError("Undeclared variable: " + node.id)
        return self.global_scope[node.id]

    def visit_StatementListNode(self, node):
        last_value = None
        for statement in node.statements:
            last_value = self.visit(statement)
        return last_value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
