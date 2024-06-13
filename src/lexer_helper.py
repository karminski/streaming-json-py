def is_ignore_token(c):
    return c in '\t\n\v\f\r '

def match_stack(stack, tokens):
    pointer = len(stack)
    tokens_left = len(tokens)
    # print(f"current pointer: {pointer}, current tokens_left: {tokens_left}")

    while True:
        tokens_left -= 1
        pointer -= 1
        if tokens_left < 0:
            break
        if pointer < 0:
            return False
        # print(f"current stack: {stack[pointer]}, current token: {tokens[tokens_left]}")
        if stack[pointer] != tokens[tokens_left]:
            return False
    return True
