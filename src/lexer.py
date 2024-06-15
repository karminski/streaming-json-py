"""
streaming-json-py main lexer method
This method will 
"""

import lexer_tokens
import lexer_helper


class Lexer:
    """
    lexer for json fragment
    """

    def __init__(self):
        self.json_content = []  # input JSON content
        # padding content for ignored characters and escape characters, etc.
        self.padding_content = []
        self.json_segment = ""  # appended JSON segment by the AppendString() method.
        self.token_stack = []  # token stack for input JSON
        self.mirror_token_stack = []  # token stack for auto-completed tokens

    def get_top_token_on_stack(self):
        """
        get token on the stack top
        """
        if not self.token_stack:
            return lexer_tokens.TOKEN_EOF
        return self.token_stack[-1]

    def get_top_token_on_mirror_stack(self):
        """
        get token on the mirror stack top
        """
        if not self.mirror_token_stack:
            return lexer_tokens.TOKEN_EOF
        return self.mirror_token_stack[-1]

    def pop_token_stack(self):
        """
        pop token on the stack top
        """
        if not self.token_stack:
            return lexer_tokens.TOKEN_EOF
        return self.token_stack.pop()

    def pop_mirror_token_stack(self):
        """
        pop token on the mirror stack top
        """
        if not self.mirror_token_stack:
            return lexer_tokens.TOKEN_EOF
        return self.mirror_token_stack.pop()

    def push_token_stack(self, token):
        """
        push token into the stack
        """
        self.token_stack.append(token)

    def push_mirror_token_stack(self, token):
        """
        push token into the mirror stack
        """
        self.mirror_token_stack.append(token)

    def dump_mirror_token_stack_to_string(self):
        """
        convert mirror stack token into string
        """
        return "".join(
            [
                lexer_tokens.token_symbol_map[x]
                for x in reversed(self.mirror_token_stack)
            ]
        )

    def skip_json_segment(self, n):
        """
        skip JSON segment by length n
        """
        self.json_segment = self.json_segment[n:]

    def push_negative_into_json_content(self):
        """
        push negative symbol `-` into JSON content
        """
        self.json_content.append(chr(lexer_tokens.TOKEN_NEGATIVE_SYMBOL))

    def push_byte_into_padding_content(self, b):
        """
        push byte into JSON content by given
        """
        self.padding_content.append(chr(b))

    def append_padding_content_to_json_content(self):
        """
        append padding content into JSON content
        """
        self.json_content.extend(self.padding_content)
        self.padding_content = []

    def have_padding_content(self):
        """
        check if padding content is empty
        """
        return bool(self.padding_content)

    def clean_padding_content(self):
        """
        set padding content to empty
        """
        self.padding_content = []

    def stream_stopped_in_an_object_key_start(self) -> bool:
        """
        check if JSON stream stopped at an object properity's key start, like `{"`
        """
        # `{`, `"` in stack, or `,`, `"` in stack
        case1 = [lexer_tokens.TOKEN_LEFT_BRACE, lexer_tokens.TOKEN_QUOTE]
        case2 = [lexer_tokens.TOKEN_COMMA, lexer_tokens.TOKEN_QUOTE]
        #  `}` in mirror stack
        case3 = [lexer_tokens.TOKEN_RIGHT_BRACE]
        return (
            lexer_helper.match_stack(self.token_stack, case1)
            or lexer_helper.match_stack(self.token_stack, case2)
        ) and lexer_helper.match_stack(self.mirror_token_stack, case3)

    def stream_stopped_in_an_object_key_end(self) -> bool:
        """
        check if JSON stream stopped in an object properity's key, like `{"field`
        """
        # // `{`, `"`, `"` in stack, or `,`, `"`, `"` in stack
        case1 = [
            lexer_tokens.TOKEN_LEFT_BRACE,
            lexer_tokens.TOKEN_QUOTE,
            lexer_tokens.TOKEN_QUOTE,
        ]
        case2 = [
            lexer_tokens.TOKEN_COMMA,
            lexer_tokens.TOKEN_QUOTE,
            lexer_tokens.TOKEN_QUOTE,
        ]
        # // `"`, `:`, `n`, `u`, `l`, `l`, `}` in mirror stack
        case3 = [
            lexer_tokens.TOKEN_RIGHT_BRACE,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N,
            lexer_tokens.TOKEN_COLON,
            lexer_tokens.TOKEN_QUOTE,
        ]
        return (
            lexer_helper.match_stack(self.token_stack, case1)
            or lexer_helper.match_stack(self.token_stack, case2)
        ) and lexer_helper.match_stack(self.mirror_token_stack, case3)

    def stream_stopped_in_an_object_string_value_start(self) -> bool:
        """
        check if JSON stream stopped in an object properity's value start,
        like `{"field": "`
        """

        # `:`, `"` in stack
        case1 = [lexer_tokens.TOKEN_COLON, lexer_tokens.TOKEN_QUOTE]
        # // `n`, `u`, `l`, `l`, `}` in mirror stack
        case2 = [
            lexer_tokens.TOKEN_RIGHT_BRACE,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N,
        ]
        return lexer_helper.match_stack(
            self.token_stack, case1
        ) and lexer_helper.match_stack(self.mirror_token_stack, case2)

    def stream_stopped_in_an_object_value_end(self) -> bool:
        """
        check if JSON stream stopped in an object properity's value finish,
        like `{"field": "value"`
        """
        # `"`, `}` left
        tokens = [lexer_tokens.TOKEN_RIGHT_BRACE, lexer_tokens.TOKEN_QUOTE]
        return lexer_helper.match_stack(self.mirror_token_stack, tokens)

    def stream_stopped_in_an_object_array_value_start(self) -> bool:
        """
        check if JSON stream stopped in an object properity's value start by array,
        like `{"field":[`
        """
        # `:`, `[` in stack
        case1 = [lexer_tokens.TOKEN_COLON, lexer_tokens.TOKEN_LEFT_BRACKET]
        # `n`, `u`, `l`, `l`, `}` in mirror stack
        case2 = [
            lexer_tokens.TOKEN_RIGHT_BRACE,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N,
        ]
        return lexer_helper.match_stack(
            self.token_stack, case1
        ) and lexer_helper.match_stack(self.mirror_token_stack, case2)

    def stream_stopped_in_an_object_object_value_start(self) -> bool:
        """
        check if JSON stream stopped in an object properity's value start by array,
        like `{"field":{`
        """
        # `:`, `{` in stack
        case1 = [lexer_tokens.TOKEN_COLON, lexer_tokens.TOKEN_LEFT_BRACE]
        # `n`, `u`, `l`, `l`, `}` in mirror stack
        case2 = [
            lexer_tokens.TOKEN_RIGHT_BRACE,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N,
        ]
        return lexer_helper.match_stack(
            self.token_stack, case1
        ) and lexer_helper.match_stack(self.mirror_token_stack, case2)

    def stream_stopped_in_an_object_negative_number_value_start(self) -> bool:
        """
        check if JSON stream stopped in an object properity's negative number value,
        like `:-`
        """
        # `:`, `-` in stack
        case1 = [lexer_tokens.TOKEN_COLON, lexer_tokens.TOKEN_NEGATIVE]
        return lexer_helper.match_stack(self.token_stack, case1)

    def stream_stopped_in_a_negative_number_value_start(self) -> bool:
        """
        check if JSON stream stopped in an object properity's negative number value,
        like `-`
        """
        # `-` in stack
        case1 = [lexer_tokens.TOKEN_NEGATIVE]
        # `0`in mirror stack
        case2 = [lexer_tokens.TOKEN_NUMBER_0]
        return lexer_helper.match_stack(
            self.token_stack, case1
        ) and lexer_helper.match_stack(self.mirror_token_stack, case2)

    def stream_stopped_in_an_array(self) -> bool:
        """
        check if JSON stream stopped in an array
        """
        return self.get_top_token_on_mirror_stack() == lexer_tokens.TOKEN_RIGHT_BRACKET

    def stream_stopped_in_an_array_string_value_end(self) -> bool:
        """
        check if JSON stream stopped in an array's string value end, like `["value"`
        """
        # `"`, `"` in stack
        case1 = [lexer_tokens.TOKEN_QUOTE, lexer_tokens.TOKEN_QUOTE]
        # `"`, `]` in mirror stack
        case2 = [lexer_tokens.TOKEN_RIGHT_BRACKET, lexer_tokens.TOKEN_QUOTE]
        return lexer_helper.match_stack(
            self.token_stack, case1
        ) and lexer_helper.match_stack(self.mirror_token_stack, case2)

    def stream_stopped_in_an_object_null_value_placeholder_start(self) -> bool:
        """
        check if JSON stream stopped in an object properity's value start by array,
        like `{"field":{`
        """
        # `n`, `u`, `l`, `l`, `}` in mirror stack
        case1 = [
            lexer_tokens.TOKEN_RIGHT_BRACE,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N,
        ]
        return lexer_helper.match_stack(self.mirror_token_stack, case1)

    def stream_stopped_in_a_string(self) -> bool:
        """
        check if JSON stream stopped in a string, like `""`
        """
        return (
            self.get_top_token_on_stack() == lexer_tokens.TOKEN_QUOTE
            and self.get_top_token_on_mirror_stack() == lexer_tokens.TOKEN_QUOTE
        )

    def stream_stopped_in_an_string_unicode_escape(self) -> bool:
        """
        check if JSON stream stopped in a string's unicode escape, like `\u0001`
        """
        # `\`, `u` in stack
        case1 = [
            lexer_tokens.TOKEN_ESCAPE_CHARACTER,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
        ]
        # `"` in mirror stack
        case2 = [lexer_tokens.TOKEN_QUOTE]
        return lexer_helper.match_stack(
            self.token_stack, case1
        ) and lexer_helper.match_stack(self.mirror_token_stack, case2)

    def stream_stopped_in_a_number(self) -> bool:
        """
        check if JSON stream stopped in a number, like `[0-9]`
        """
        return self.get_top_token_on_stack() == lexer_tokens.TOKEN_NUMBER

    def stream_stopped_in_a_number_decimal_part(self) -> bool:
        """
        check if JSON stream stopped in a number first decimal place, like `.?`
        """
        # `.`, lexer_tokens.TOKEN_NUMBER in stack
        return self.get_top_token_on_stack() == lexer_tokens.TOKEN_DOT

    def stream_stopped_in_a_number_decimal_part_middle(self) -> bool:
        """
        check if JSON stream stopped in a number other decimal place (except first place),
        like `.[0-9]?`
        """
        case1 = [lexer_tokens.TOKEN_DOT, lexer_tokens.TOKEN_NUMBER]
        return lexer_helper.match_stack(self.token_stack, case1)

    def stream_stopped_with_leading_escape_character(self) -> bool:
        """
        check if JSON stream stopped in escape character, like `\`
        """
        return self.get_top_token_on_stack() == lexer_tokens.TOKEN_ESCAPE_CHARACTER

    def match_token(self):
        """
        lexer match JSON token method, convert JSON segment to JSON tokens
        """
        # Segment end
        if len(self.json_segment) == 0:
            return lexer_tokens.TOKEN_EOF, 0

        token_symbol = self.json_segment[0]

        # Check if ignored token
        if lexer_helper.is_ignore_token(token_symbol):
            self.skip_json_segment(1)
            return lexer_tokens.TOKEN_IGNORED, token_symbol
        # Match token
        token_mapping = {
            lexer_tokens.TOKEN_LEFT_BRACKET_SYMBOL: lexer_tokens.TOKEN_LEFT_BRACKET,
            lexer_tokens.TOKEN_RIGHT_BRACKET_SYMBOL: lexer_tokens.TOKEN_RIGHT_BRACKET,
            lexer_tokens.TOKEN_LEFT_BRACE_SYMBOL: lexer_tokens.TOKEN_LEFT_BRACE,
            lexer_tokens.TOKEN_RIGHT_BRACE_SYMBOL: lexer_tokens.TOKEN_RIGHT_BRACE,
            lexer_tokens.TOKEN_COLON_SYMBOL: lexer_tokens.TOKEN_COLON,
            lexer_tokens.TOKEN_DOT_SYMBOL: lexer_tokens.TOKEN_DOT,
            lexer_tokens.TOKEN_COMMA_SYMBOL: lexer_tokens.TOKEN_COMMA,
            lexer_tokens.TOKEN_QUOTE_SYMBOL: lexer_tokens.TOKEN_QUOTE,
            lexer_tokens.TOKEN_ESCAPE_CHARACTER_SYMBOL: lexer_tokens.TOKEN_ESCAPE_CHARACTER,
            lexer_tokens.TOKEN_SLASH_SYMBOL: lexer_tokens.TOKEN_SLASH,
            lexer_tokens.TOKEN_NEGATIVE_SYMBOL: lexer_tokens.TOKEN_NEGATIVE,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_A_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_A,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_B_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_B,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_C_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_C,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_D_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_D,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_F_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_F,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_R_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_R,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_S_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_S,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_T_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_T,
            lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U_SYMBOL: lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
            lexer_tokens.TOKEN_ALPHABET_UPPERCASE_A_SYMBOL: lexer_tokens.TOKEN_ALPHABET_UPPERCASE_A,
            lexer_tokens.TOKEN_ALPHABET_UPPERCASE_B_SYMBOL: lexer_tokens.TOKEN_ALPHABET_UPPERCASE_B,
            lexer_tokens.TOKEN_ALPHABET_UPPERCASE_C_SYMBOL: lexer_tokens.TOKEN_ALPHABET_UPPERCASE_C,
            lexer_tokens.TOKEN_ALPHABET_UPPERCASE_D_SYMBOL: lexer_tokens.TOKEN_ALPHABET_UPPERCASE_D,
            lexer_tokens.TOKEN_ALPHABET_UPPERCASE_E_SYMBOL: lexer_tokens.TOKEN_ALPHABET_UPPERCASE_E,
            lexer_tokens.TOKEN_ALPHABET_UPPERCASE_F_SYMBOL: lexer_tokens.TOKEN_ALPHABET_UPPERCASE_F,
            lexer_tokens.TOKEN_NUMBER_0_SYMBOL: lexer_tokens.TOKEN_NUMBER_0,
            lexer_tokens.TOKEN_NUMBER_1_SYMBOL: lexer_tokens.TOKEN_NUMBER_1,
            lexer_tokens.TOKEN_NUMBER_2_SYMBOL: lexer_tokens.TOKEN_NUMBER_2,
            lexer_tokens.TOKEN_NUMBER_3_SYMBOL: lexer_tokens.TOKEN_NUMBER_3,
            lexer_tokens.TOKEN_NUMBER_4_SYMBOL: lexer_tokens.TOKEN_NUMBER_4,
            lexer_tokens.TOKEN_NUMBER_5_SYMBOL: lexer_tokens.TOKEN_NUMBER_5,
            lexer_tokens.TOKEN_NUMBER_6_SYMBOL: lexer_tokens.TOKEN_NUMBER_6,
            lexer_tokens.TOKEN_NUMBER_7_SYMBOL: lexer_tokens.TOKEN_NUMBER_7,
            lexer_tokens.TOKEN_NUMBER_8_SYMBOL: lexer_tokens.TOKEN_NUMBER_8,
            lexer_tokens.TOKEN_NUMBER_9_SYMBOL: lexer_tokens.TOKEN_NUMBER_9,
        }

        token_result = token_mapping.get(token_symbol, lexer_tokens.TOKEN_OTHERS)
        self.skip_json_segment(1)
        return token_result, token_symbol

    def append_string(self, string):
        """
        append JSON string to current JSON stream content
        this method will traversal all token and generate mirror token for complete full JSON
        """

        self.json_segment = string
        while True:
            token, token_symbol = self.match_token()

            if token == lexer_tokens.TOKEN_EOF:
                # nothing to do with TOKEN_EOF
                pass
            elif token == lexer_tokens.TOKEN_IGNORED:
                if self.stream_stopped_in_a_string():
                    self.json_content += token_symbol
                    continue
                self.push_byte_into_padding_content(token_symbol)
            elif token == lexer_tokens.TOKEN_OTHERS:
                # check if json stream stopped with padding content
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                # write current token symbol to JSON content
                self.json_content += token_symbol
            elif token == lexer_tokens.TOKEN_LEFT_BRACKET:
                # check if json stream stopped with padding content
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                self.json_content += token_symbol
                if self.stream_stopped_in_a_string():
                    continue
                self.push_token_stack(token)
                if self.stream_stopped_in_an_object_array_value_start():
                    # pop `n`, `u`, `l`, `l` from mirror stack
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                # push `]` into mirror stack
                self.push_mirror_token_stack(lexer_tokens.TOKEN_RIGHT_BRACKET)
            elif token == lexer_tokens.TOKEN_RIGHT_BRACKET:
                if self.stream_stopped_in_a_string():
                    self.json_content += token_symbol
                    continue
                # check if json stream stopped with padding content
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                # write current token symbol to JSON content
                self.json_content += token_symbol
                # push `]` into stack
                self.push_token_stack(token)
                # pop `]` from mirror stack
                self.pop_mirror_token_stack()
            elif token == lexer_tokens.TOKEN_LEFT_BRACE:
                # check if json stream stopped with padding content
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                # write current token symbol to JSON content
                self.json_content += token_symbol
                if self.stream_stopped_in_a_string():
                    continue
                self.push_token_stack(token)
                if self.stream_stopped_in_an_object_object_value_start():
                    # pop `n`, `u`, `l`, `l` from mirror stack
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                # push `}` into mirror stack
                self.push_mirror_token_stack(lexer_tokens.TOKEN_RIGHT_BRACE)
            elif token == lexer_tokens.TOKEN_RIGHT_BRACE:
                if self.stream_stopped_in_a_string():
                    self.json_content += token_symbol
                    continue
                # check if json stream stopped with padding content
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                self.json_content += token_symbol
                # push `}` into stack
                self.push_token_stack(token)
                # pop `}` from mirror stack
                self.pop_mirror_token_stack()
            elif token == lexer_tokens.TOKEN_QUOTE:
                # check if escape quote `\"`
                if self.stream_stopped_with_leading_escape_character():
                    # push padding escape character `\` into JSON content
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                    # write current token symbol to JSON content
                    self.json_content += token_symbol
                    # pop `\` from  stack
                    self.pop_token_stack()
                    continue
                # check if json stream stopped with padding content
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()

                # write current token symbol to JSON content
                self.json_content += token_symbol
                self.push_token_stack(token)
                if self.stream_stopped_in_an_array():
                    # push `"` into mirror stack
                    self.push_mirror_token_stack(lexer_tokens.TOKEN_QUOTE)
                elif self.stream_stopped_in_an_array_string_value_end():
                    # pop `"` from mirror stack
                    self.pop_mirror_token_stack()
                elif self.stream_stopped_in_an_object_key_start():
                    #  check if stopped in key of object's properity or value of object's properity
                    #  push `"`, `:`, `n`, `u`, `l`, `l` into mirror stack
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N
                    )
                    self.push_mirror_token_stack(lexer_tokens.TOKEN_COLON)
                    self.push_mirror_token_stack(lexer_tokens.TOKEN_QUOTE)
                elif self.stream_stopped_in_an_object_key_end():
                    # check if stopped in key of object's properity or value of object's properity
                    # pop `"` from mirror stack
                    self.pop_mirror_token_stack()
                elif self.stream_stopped_in_an_object_string_value_start():
                    # pop `n`, `u`, `l`, `l` from mirror stack
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    # push `"` into mirror stack
                    self.push_mirror_token_stack(lexer_tokens.TOKEN_QUOTE)
                elif self.stream_stopped_in_an_object_value_end():
                    # pop `"` from mirror stack
                    self.pop_mirror_token_stack()
                else:
                    return "Invalid quote token in JSON stream"
            elif token == lexer_tokens.TOKEN_COLON:
                if self.stream_stopped_in_a_string():
                    self.json_content += token_symbol
                    continue
                # check if json stream stopped with padding content
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                # write current token symbol to JSON content
                self.json_content += token_symbol
                self.push_token_stack(token)
                # pop `:` from mirror stack
                self.pop_mirror_token_stack()
            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_A:
                # as hex in unicode
                if self.stream_stopped_in_an_string_unicode_escape():
                    self.push_byte_into_padding_content(token_symbol)
                    # check if unicode escape is full length
                    if len(self.padding_content) == 6:
                        self.append_padding_content_to_json_content()
                        self.clean_padding_content()
                        # pop `\`, `u` from stack
                        self.pop_token_stack()
                        self.pop_token_stack()
                    continue
                # write current token symbol to JSON content
                self.json_content += token_symbol
                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # check if `f` in token stack and `a`, `l`, `s`, `e in mirror stack
                def it_is_part_of_token_false():
                    left = [lexer_tokens.TOKEN_ALPHABET_LOWERCASE_F]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_S,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_A,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                if not it_is_part_of_token_false():
                    continue

                self.push_token_stack(token)
                self.pop_mirror_token_stack()
            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_B:
                # as hex in unicode
                if self.stream_stopped_in_an_string_unicode_escape():
                    self.push_byte_into_padding_content(token_symbol)
                    # check if unicode escape is full length
                    if len(self.padding_content) == 6:
                        self.append_padding_content_to_json_content()
                        self.clean_padding_content()
                        # pop `\`, `u` from stack
                        self.pop_token_stack()
                        self.pop_token_stack()
                    continue

                # \b escape `\`, `b`
                if self.stream_stopped_with_leading_escape_character():
                    # push padding escape character `\` into JSON content
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                    # write current token symbol to JSON content
                    self.json_content += token_symbol
                    # pop `\` from  stack
                    self.pop_token_stack()
                    continue

                # write current token symbol to JSON content
                self.json_content += token_symbol

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E:
                # as hex in unicode
                if self.stream_stopped_in_an_string_unicode_escape():
                    self.push_byte_into_padding_content(token_symbol)
                    # check if unicode escape is full length
                    if len(self.padding_content) == 6:
                        self.append_padding_content_to_json_content()
                        self.clean_padding_content()
                        # pop `\`, `u` from stack
                        self.pop_token_stack()
                        self.pop_token_stack()
                    continue

                # check if in a number, as `e` (exponent) in scientific notation
                if self.stream_stopped_in_a_number_decimal_part_middle():
                    self.push_byte_into_padding_content(token_symbol)
                    continue

                # write current token symbol to JSON content
                self.json_content += token_symbol

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # check if `f`, `a`, `l`, `s` in token stack and `e` in mirror stack
                def it_is_part_of_token_false():
                    left = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_F,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_A,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_S,
                    ]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                # check if `t`, `r`, `u` in token stack and `e` in mirror stack
                def it_is_part_of_token_true():
                    left = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_T,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_R,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
                    ]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                if not it_is_part_of_token_false() and not it_is_part_of_token_true():
                    continue

                self.push_token_stack(token)
                self.pop_mirror_token_stack()
            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_F:
                # as hex in unicode
                if self.stream_stopped_in_an_string_unicode_escape():
                    self.push_byte_into_padding_content(token_symbol)
                    # check if unicode escape is full length
                    if len(self.padding_content) == 6:
                        self.append_padding_content_to_json_content()
                        self.clean_padding_content()
                        # pop `\`, `u` from stack
                        self.pop_token_stack()
                        self.pop_token_stack()
                    continue

                # \f escape `\`, `f`
                if self.stream_stopped_with_leading_escape_character():
                    # push padding escape character `\` into JSON content
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                    # write current token symbol to JSON content
                    self.json_content.append(token_symbol)
                    # pop `\` from  stack
                    self.pop_token_stack()
                    continue

                # check if json stream stopped with padding content, like case `[true , f`
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()

                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # push `f` into stack
                self.push_token_stack(token)
                if self.stream_stopped_in_an_array():
                    #  in array
                    #  push `a`, `l`, `s`, `e`
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_S
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_A
                    )
                else:
                    # in object
                    # pop `n`, `u`, `l`, `l`
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    # push `a`, `l`, `s`, `e`
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_S
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_A
                    )

            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L:
                # write current token symbol to JSON content
                self.json_content.append(token_symbol)
                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # check if `f`, `a` in token stack and, `l`, `s`, `e` in mirror stack
                def it_is_part_of_token_false():
                    left = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_F,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_A,
                    ]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_S,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                # check if `n`, `u` in token stack and `l`, `l` in mirror stack
                def it_is_part_of_token_null1():
                    left = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
                    ]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                # check if `n`, `u`, `l` in token stack and `l` in mirror stack
                def it_is_part_of_token_null2():
                    left = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                    ]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                if (
                    not it_is_part_of_token_false()
                    and not it_is_part_of_token_null1()
                    and not it_is_part_of_token_null2()
                ):
                    continue

                self.push_token_stack(token)
                self.pop_mirror_token_stack()

            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N:
                # \n escape `\`, `n`
                if self.stream_stopped_with_leading_escape_character():
                    # push padding escape character `\` into JSON content
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                    # write current token symbol to JSON content
                    self.json_content.append(token_symbol)
                    # pop `\` from  stack
                    self.pop_token_stack()
                    continue

                # check if json stream stopped with padding content, like case `[true , n`
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()

                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # push `n`
                self.push_token_stack(token)
                if self.stream_stopped_in_an_array():
                    # in array, push `u`, `l`, `l`
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U
                    )
                else:
                    # in object, pop `n`
                    self.pop_mirror_token_stack()

            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_R:
                # \r escape `\`, `r`
                if self.stream_stopped_with_leading_escape_character():
                    # push padding escape character `\` into JSON content
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                    # write current token symbol to JSON content
                    self.json_content.append(token_symbol)
                    # pop `\` from  stack
                    self.pop_token_stack()
                    continue

                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # check if `t` in token stack and `r`, `u`, `e in mirror stack
                def it_is_part_of_token_true():
                    left = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_T,
                    ]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_R,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                if not it_is_part_of_token_true():
                    continue

                self.push_token_stack(token)
                self.pop_mirror_token_stack()

            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_S:
                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # check if `f`, `a`, `l` in token stack and `s`, `e in mirror stack
                def it_is_part_of_token_false():
                    left = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_F,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_A,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                    ]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_S,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                if not it_is_part_of_token_false():
                    continue

                self.push_token_stack(token)
                self.pop_mirror_token_stack()

            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_T:
                # \t escape `\`, `t`
                if self.stream_stopped_with_leading_escape_character():
                    # push padding escape character `\` into JSON content
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                    # write current token symbol to JSON content
                    self.json_content.append(token_symbol)
                    # pop `\` from  stack
                    self.pop_token_stack()
                    continue

                # check if json stream stopped with padding content, like case `[true , t`
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()

                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # push `t` to stack
                self.push_token_stack(token)
                if self.stream_stopped_in_an_array():
                    # in array
                    # push `r`, `u`, `e`
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_R
                    )
                else:
                    # in object
                    # pop `n`, `u`, `l`, `l`
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    # push `r`, `u`, `e`
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U
                    )
                    self.push_mirror_token_stack(
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_R
                    )

            elif token == lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U:
                # unicode escape `\`, `u`
                if self.stream_stopped_with_leading_escape_character():
                    self.push_token_stack(token)
                    self.padding_content.append(token_symbol)
                    continue

                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # check if `t`, `r` in token stack and, `u`, `e` in mirror stack
                def it_is_part_of_token_true():
                    left = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_T,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_R,
                    ]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_E,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                # check if `n` in token stack and `u`, `l`, `l` in mirror stack
                def it_is_part_of_token_null():
                    left = [lexer_tokens.TOKEN_ALPHABET_LOWERCASE_N]
                    right = [
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_L,
                        lexer_tokens.TOKEN_ALPHABET_LOWERCASE_U,
                    ]
                    return lexer_helper.match_stack(
                        self.token_stack, left
                    ) and lexer_helper.match_stack(self.mirror_token_stack, right)

                if not it_is_part_of_token_true() and not it_is_part_of_token_null():
                    continue

                self.push_token_stack(token)
                self.pop_mirror_token_stack()

            elif token in [
                lexer_tokens.TOKEN_ALPHABET_UPPERCASE_A,
                lexer_tokens.TOKEN_ALPHABET_UPPERCASE_B,
                lexer_tokens.TOKEN_ALPHABET_UPPERCASE_C,
                lexer_tokens.TOKEN_ALPHABET_UPPERCASE_D,
                lexer_tokens.TOKEN_ALPHABET_LOWERCASE_C,
                lexer_tokens.TOKEN_ALPHABET_LOWERCASE_D,
                lexer_tokens.TOKEN_ALPHABET_UPPERCASE_F,
            ]:
                # as hex in unicode
                if self.stream_stopped_in_an_string_unicode_escape():
                    self.push_byte_into_padding_content(token_symbol)
                    # check if unicode escape is full length
                    if self.padding_content.Len() == 6:
                        self.append_padding_content_to_json_content()
                        self.clean_padding_content()
                        # pop `\`, `u` from stack
                        self.pop_token_stack()
                        self.pop_token_stack()
                    continue

                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

            elif token == lexer_tokens.TOKEN_ALPHABET_UPPERCASE_E:
                # as hex in unicode
                if self.stream_stopped_in_an_string_unicode_escape():
                    self.push_byte_into_padding_content(token_symbol)
                    # check if unicode escape is full length
                    if len(self.padding_content) == 6:
                        self.append_padding_content_to_json_content()
                        self.clean_padding_content()
                        # pop `\`, `u` from stack
                        self.pop_token_stack()
                        self.pop_token_stack()
                    continue

                # check if in a number, as `E` (exponent) in scientific notation
                if self.stream_stopped_in_a_number_decimal_part_middle():
                    self.push_byte_into_padding_content(token_symbol)
                    continue

                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue
            elif token in [
                lexer_tokens.TOKEN_NUMBER_0,
                lexer_tokens.TOKEN_NUMBER_1,
                lexer_tokens.TOKEN_NUMBER_2,
                lexer_tokens.TOKEN_NUMBER_3,
                lexer_tokens.TOKEN_NUMBER_4,
                lexer_tokens.TOKEN_NUMBER_5,
                lexer_tokens.TOKEN_NUMBER_6,
                lexer_tokens.TOKEN_NUMBER_7,
                lexer_tokens.TOKEN_NUMBER_8,
                lexer_tokens.TOKEN_NUMBER_9,
            ]:
                # as number in unicode
                if self.stream_stopped_in_an_string_unicode_escape():
                    self.push_byte_into_padding_content(token_symbol)
                    # check if unicode escape is full length
                    if len(self.padding_content) == 6:
                        self.append_padding_content_to_json_content()
                        self.clean_padding_content()
                        #  pop `\`, `u` from stack
                        self.pop_token_stack()
                        self.pop_token_stack()
                    continue

                # check if json stream stopped with padding content, like `[1 , 1`
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()

                # in negative part of a number
                if self.stream_stopped_in_a_negative_number_value_start():
                    self.push_negative_into_json_content()
                    # pop `0` from mirror stack
                    self.pop_mirror_token_stack()

                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string or a number, just skip token
                if (
                    self.stream_stopped_in_a_string()
                    or self.stream_stopped_in_a_number()
                ):
                    continue

                # in decimal part of a number
                if self.stream_stopped_in_a_number_decimal_part():
                    self.push_token_stack(lexer_tokens.TOKEN_NUMBER)
                    # pop placeholder `0` in decimal part
                    self.pop_mirror_token_stack()
                    continue

                # first number type token, push token into stack
                self.push_token_stack(lexer_tokens.TOKEN_NUMBER)

                # check if we are in an object or an array
                if self.stream_stopped_in_an_array():
                    continue
                elif self.stream_stopped_in_an_object_null_value_placeholder_start():
                    # pop `n`, `u`, `l`, `l`
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()

            elif token == lexer_tokens.TOKEN_COMMA:
                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    self.json_content.append(token_symbol)
                    continue
                # in a object or a array, keep the comma in stack but not write it into JSONContent, until next token arrival
                # the comma must following with token: quote, null, true, false, number
                self.push_byte_into_padding_content(token_symbol)
                self.push_token_stack(token)
            elif token == lexer_tokens.TOKEN_DOT:
                # write current token symbol to JSON content
                self.json_content.append(token_symbol)

                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    continue

                # use 0 for decimal part place holder
                self.push_token_stack(token)
                self.push_mirror_token_stack(lexer_tokens.TOKEN_NUMBER_0)

            elif token == lexer_tokens.TOKEN_SLASH:
                #  escape character `\`, `/`
                if self.stream_stopped_with_leading_escape_character():
                    # push padding escape character `\` into JSON content
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                    # write current token symbol to JSON content
                    self.json_content.append(token_symbol)
                    # pop `\` from  stack
                    self.pop_token_stack()
                    continue

            elif token == lexer_tokens.TOKEN_ESCAPE_CHARACTER:
                # double escape character `\`, `\`
                if self.stream_stopped_with_leading_escape_character():
                    # push padding escape character `\` into JSON content
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()
                    # write current token symbol to JSON content
                    self.json_content.append(token_symbol)
                    # pop `\` from  stack
                    self.pop_token_stack()
                    continue

                # just write escape character into stack and waitting other token trigger escape method.
                self.push_token_stack(token)
                self.push_byte_into_padding_content(
                    lexer_tokens.TOKEN_ESCAPE_CHARACTER_SYMBOL
                )
            elif token == lexer_tokens.TOKEN_NEGATIVE:
                # in a string, just skip token
                if self.stream_stopped_in_a_string():
                    self.json_content.append(token_symbol)
                    continue

                # check if json stream stopped with padding content, like `[1 , -`
                if self.have_padding_content():
                    self.append_padding_content_to_json_content()
                    self.clean_padding_content()

                # just write negative character into stack and waitting other token trigger it.
                self.push_token_stack(token)
                if self.stream_stopped_in_an_object_negative_number_value_start():
                    # pop `n`, `u`, `l`, `l` from mirror stack
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()
                    self.pop_mirror_token_stack()

                # push `0` into mirror stack for placeholder
                self.push_mirror_token_stack(lexer_tokens.TOKEN_NUMBER_0)

            else:
                return f"Unexpected token: {token}, token symbol: {token_symbol}"

            if token == lexer_tokens.TOKEN_EOF:
                break

        return None

    def complete_json(self):
        """
        complete the incomplete JSON string by concat JSON content and mirror tokens
        """
        # This combines json_content and mirror token stack into a complete JSON string
        return "".join(self.json_content) + self.dump_mirror_token_stack_to_string()
