from rich import print
import sys

from src.env import create_env
from src.interpreter import Interpreter
from src.lexer import Lexer
from src.parser import Parser


def run(code):
    env = create_env()
    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    return result


def test_file(filename):
    with open(f"./examples/calc/{filename}") as f:
        print(run(f.read()))


def run_tests():
    assert run("2 * 3 + 1") == 7
    assert run("5 * 3 + 4 + 2 % 2 * 8") == 19
    assert run("7 + 3 * (10 / (12 / (3 + 1) - 1))") == 22
    assert run("7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)") == 10
    assert run("7 + (((3 + 2)))") == 12

    assert run("- 3") == -3
    assert run("+ 3") == 3
    assert run("5 - - - + - 3") == 8
    assert run("5 - - - + - (3 + 4) - +2") == 10


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(run("1 + 2"))
    elif sys.argv[1] == "-t":
        print("Running tests -----")
        run_tests()
    elif sys.argv[1] == "-i":
        while True:
            try:
                text = input("lang> ")
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            if not text:
                continue

            try:
                print(run(text))
            except Exception as e:
                print(e)
