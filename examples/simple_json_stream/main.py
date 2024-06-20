import streamingjson


def main():
    # Case A, complete the incomplete JSON object
    json_segment_a = '{"a":'  # will complete to `{"a":null}`
    lexer = streamingjson.Lexer()
    lexer.append_string(json_segment_a)
    completed_json = lexer.complete_json()
    print(f"completedJSON: {completed_json}")

    # Case B, complete the incomplete JSON array
    json_segment_b = "[t"  # will complete to `[true]`
    lexer = streamingjson.Lexer()
    lexer.append_string(json_segment_b)
    completed_json = lexer.complete_json()
    print(f"completedJSON: {completed_json}")


if __name__ == "__main__":
    main()
