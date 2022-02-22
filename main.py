from rich import print
import sys

from src.interpreter import Interpreter
from src.lexer import Lexer
from src.parser import Parser
import readline  # Necessary to have a nice python input()


def run(code):
    if code == "print_scope()":
        print()

    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    return result


def test_file(filename):
    with open(f"./examples/{filename}") as f:
        print("\nReturned value:", run(f.read()))


def repl():
    shared_scope = {}
    while True:
        try:
            code = input("hufl> ")
            if code == "print_scope()":
                print(shared_scope)
                continue
            if not code:
                continue
            lexer = Lexer(code)
            parser = Parser(lexer)
            interpreter = Interpreter(parser, shared_scope)
            result = interpreter.interpret()
            print(result)
            shared_scope = interpreter.global_scope
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            # print(e)
            raise e


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()

    elif sys.argv[1] == "-t":
        print("Running tests...")
        print("...jk")

    elif sys.argv[1] == "-f" and len(sys.argv) == 3:
        test_file(sys.argv[2])
