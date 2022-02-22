from src.token import Token


RESERVED_KEYWORDS = {
    "let": Token("LET", "LET", 0, 0),
    "def": Token("DEF", "DEF", 0, 0),
    "match": Token("MATCH", "MATCH", 0, 0),
    "true": Token("BOOLEAN", True, 0, 0),
    "false": Token("BOOLEAN", False, 0, 0),
    "and": Token("AND", "AND", 0, 0),
    "or": Token("OR", "OR", 0, 0),
}
