from src.token import Token


RESERVED_KEYWORDS = {
    "let": Token("LET", "LET", 0, 0),
    "fn": Token("FN", "FN", 0, 0),
    "match": Token("MATCH", "MATCH", 0, 0),
    "true": Token("BOOLEAN", True, 0, 0),
    "false": Token("BOOLEAN", False, 0, 0),
    "and": Token("AND", "AND", 0, 0),
    "or": Token("OR", "OR", 0, 0),
    "if": Token("IF", "IF", 0, 0),
    "elif": Token("ELIF", "ELIF", 0, 0),
    "else": Token("ELSE", "ELSE", 0, 0),
}
