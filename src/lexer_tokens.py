# Token constants
TOKEN_EOF = 0  # end-of-file
TOKEN_IGNORED = 1  # \t', '\n', '\v', '\f', '\r', ' '
TOKEN_LEFT_BRACKET = 2  # [
TOKEN_RIGHT_BRACKET = 3  # ]
TOKEN_LEFT_BRACE = 4  # {
TOKEN_RIGHT_BRACE = 5  # }
TOKEN_COLON = 6  # :
TOKEN_DOT = 7  # .
TOKEN_COMMA = 8  # ,
TOKEN_QUOTE = 9  # "
TOKEN_ESCAPE_CHARACTER = 10  # \
TOKEN_SLASH = 11  # /
TOKEN_NEGATIVE = 12  # -
TOKEN_NULL = 13  # null
TOKEN_TRUE = 14  # true
TOKEN_FALSE = 15  # false
TOKEN_ALPHABET_LOWERCASE_A = 16  # a
TOKEN_ALPHABET_LOWERCASE_B = 17  # b
TOKEN_ALPHABET_LOWERCASE_C = 18  # c
TOKEN_ALPHABET_LOWERCASE_D = 19  # d
TOKEN_ALPHABET_LOWERCASE_E = 20  # e
TOKEN_ALPHABET_LOWERCASE_F = 21  # f
TOKEN_ALPHABET_LOWERCASE_L = 22  # l
TOKEN_ALPHABET_LOWERCASE_N = 23  # n
TOKEN_ALPHABET_LOWERCASE_R = 24  # r
TOKEN_ALPHABET_LOWERCASE_S = 25  # s
TOKEN_ALPHABET_LOWERCASE_T = 26  # t
TOKEN_ALPHABET_LOWERCASE_U = 27  # u
TOKEN_ALPHABET_UPPERCASE_A = 28  # A
TOKEN_ALPHABET_UPPERCASE_B = 29  # B
TOKEN_ALPHABET_UPPERCASE_C = 30  # C
TOKEN_ALPHABET_UPPERCASE_D = 31  # D
TOKEN_ALPHABET_UPPERCASE_E = 32  # E
TOKEN_ALPHABET_UPPERCASE_F = 33  # F
TOKEN_NUMBER = 34  # number
TOKEN_NUMBER_0 = 35  # 0
TOKEN_NUMBER_1 = 36  # 1
TOKEN_NUMBER_2 = 37  # 2
TOKEN_NUMBER_3 = 38  # 3
TOKEN_NUMBER_4 = 39  # 4
TOKEN_NUMBER_5 = 40  # 5
TOKEN_NUMBER_6 = 41  # 6
TOKEN_NUMBER_7 = 42  # 7
TOKEN_NUMBER_8 = 43  # 8
TOKEN_NUMBER_9 = 44  # 9
TOKEN_OTHERS = 45  # anything else in json

# Token Symbols
TOKEN_LEFT_BRACKET_SYMBOL         = '['
TOKEN_RIGHT_BRACKET_SYMBOL        = ']'
TOKEN_LEFT_BRACE_SYMBOL           = '{'
TOKEN_RIGHT_BRACE_SYMBOL          = '}'
TOKEN_COLON_SYMBOL                = ':'
TOKEN_DOT_SYMBOL                  = '.'
TOKEN_COMMA_SYMBOL                = ','
TOKEN_QUOTE_SYMBOL                = '"'
TOKEN_ESCAPE_CHARACTER_SYMBOL     = '\\'
TOKEN_SLASH_SYMBOL                = '/'
TOKEN_NEGATIVE_SYMBOL             = '-'
TOKEN_ALPHABET_LOWERCASE_A_SYMBOL = 'a'
TOKEN_ALPHABET_LOWERCASE_B_SYMBOL = 'b'
TOKEN_ALPHABET_LOWERCASE_C_SYMBOL = 'c'
TOKEN_ALPHABET_LOWERCASE_D_SYMBOL = 'd'
TOKEN_ALPHABET_LOWERCASE_E_SYMBOL = 'e'
TOKEN_ALPHABET_LOWERCASE_F_SYMBOL = 'f'
TOKEN_ALPHABET_LOWERCASE_L_SYMBOL = 'l'
TOKEN_ALPHABET_LOWERCASE_N_SYMBOL = 'n'
TOKEN_ALPHABET_LOWERCASE_R_SYMBOL = 'r'
TOKEN_ALPHABET_LOWERCASE_S_SYMBOL = 's'
TOKEN_ALPHABET_LOWERCASE_T_SYMBOL = 't'
TOKEN_ALPHABET_LOWERCASE_U_SYMBOL = 'u'
TOKEN_ALPHABET_UPPERCASE_A_SYMBOL = 'A'
TOKEN_ALPHABET_UPPERCASE_B_SYMBOL = 'B'
TOKEN_ALPHABET_UPPERCASE_C_SYMBOL = 'C'
TOKEN_ALPHABET_UPPERCASE_D_SYMBOL = 'D'
TOKEN_ALPHABET_UPPERCASE_E_SYMBOL = 'E'
TOKEN_ALPHABET_UPPERCASE_F_SYMBOL = 'F'
TOKEN_NUMBER_0_SYMBOL             = '0'
TOKEN_NUMBER_1_SYMBOL             = '1'
TOKEN_NUMBER_2_SYMBOL             = '2'
TOKEN_NUMBER_3_SYMBOL             = '3'
TOKEN_NUMBER_4_SYMBOL             = '4'
TOKEN_NUMBER_5_SYMBOL             = '5'
TOKEN_NUMBER_6_SYMBOL             = '6'
TOKEN_NUMBER_7_SYMBOL             = '7'
TOKEN_NUMBER_8_SYMBOL             = '8'
TOKEN_NUMBER_9_SYMBOL             = '9'


# Token symbol map
token_symbol_map = {
    TOKEN_EOF: "EOF",
    TOKEN_LEFT_BRACKET: "[",
    TOKEN_RIGHT_BRACKET: "]",
    TOKEN_LEFT_BRACE: "{",
    TOKEN_RIGHT_BRACE: "}",
    TOKEN_COLON: ":",
    TOKEN_DOT: ".",
    TOKEN_COMMA: ",",
    TOKEN_QUOTE: "\"",
    TOKEN_ESCAPE_CHARACTER: "\\",
    TOKEN_SLASH: "/",
    TOKEN_NEGATIVE: "-",
    TOKEN_NULL: "null",
    TOKEN_TRUE: "true",
    TOKEN_FALSE: "false",
    TOKEN_ALPHABET_LOWERCASE_A: "a",
    TOKEN_ALPHABET_LOWERCASE_B: "b",
    TOKEN_ALPHABET_LOWERCASE_C: "c",
    TOKEN_ALPHABET_LOWERCASE_D: "d",
    TOKEN_ALPHABET_LOWERCASE_E: "e",
    TOKEN_ALPHABET_LOWERCASE_F: "f",
    TOKEN_ALPHABET_LOWERCASE_L: "l",
    TOKEN_ALPHABET_LOWERCASE_N: "n",
    TOKEN_ALPHABET_LOWERCASE_R: "r",
    TOKEN_ALPHABET_LOWERCASE_S: "s",
    TOKEN_ALPHABET_LOWERCASE_T: "t",
    TOKEN_ALPHABET_LOWERCASE_U: "u",
    TOKEN_ALPHABET_UPPERCASE_A: "A",
    TOKEN_ALPHABET_UPPERCASE_B: "B",
    TOKEN_ALPHABET_UPPERCASE_C: "C",
    TOKEN_ALPHABET_UPPERCASE_D: "D",
    TOKEN_ALPHABET_UPPERCASE_E: "E",
    TOKEN_ALPHABET_UPPERCASE_F: "F",
    TOKEN_NUMBER_0: "0",
    TOKEN_NUMBER_1: "1",
    TOKEN_NUMBER_2: "2",
    TOKEN_NUMBER_3: "3",
    TOKEN_NUMBER_4: "4",
    TOKEN_NUMBER_5: "5",
    TOKEN_NUMBER_6: "6",
    TOKEN_NUMBER_7: "7",
    TOKEN_NUMBER_8: "8",
    TOKEN_NUMBER_9: "9",
}
