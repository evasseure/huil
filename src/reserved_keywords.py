from src.token import Token


RESERVED_KEYWORDS = {
    "let": Token("LET", "LET", 0, 0),
    "def": Token("DEF", "DEF", 0, 0),
    "match": Token("MATCH", "MATCH", 0, 0),
}
