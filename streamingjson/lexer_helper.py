"""
helper method for lexer
"""


def is_ignore_token(c):
    """
    check if target character is ignore token
    """
    return c in "\t\n\v\f\r "


def match_stack(stack, tokens):
    """
    check if target stack match given tokens
    """
    pointer = len(stack)
    tokens_left = len(tokens)

    while True:
        tokens_left -= 1
        pointer -= 1
        if tokens_left < 0:
            break
        if pointer < 0:
            return False
        if stack[pointer] != tokens[tokens_left]:
            return False
    return True
