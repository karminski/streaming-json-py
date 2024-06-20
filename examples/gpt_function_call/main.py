import streamingjson


# In GPT's chat completion stream mode, the request for tool_calls returns a structure as follows:
#
# {
#     "id": "chatcmpl-?",
#     "object": "chat.completion.chunk",
#     "created": 1712000001,
#     "model": "gpt-4-0125-preview",
#     "system_fingerprint": "fp_?",
#     "choices": [
#         {
#             "index": 0,
#             "delta": {
#                 "tool_calls": [
#                     {
#                         "index": 0,
#                         "function": {
#                             "arguments": "{\"fi"
#                         }
#                     }
#                 ]
#             },
#             "logprobs": null,
#             "finish_reason": null
#         }
#     ]
# }
#
# We need extract data.choices[0].delta.tool_calls[0].function.arguments.
# The arguments fiels is a JSON fragment, we can use steaming-json-go complete it to a syntactically correct JSON and Unmarshal it.


def main():
    # We use string slice to simulate the arguments field in the return of GPT.
    arguments = [
        '{"fu',
        "nction",
        "_name",
        '"',
        ":",
        '"run',
        "_code",
        '", ',
        '"argu',
        'ments"',
        ": ",
        '"print(',
        '\\"hello',
        " world",
        '\\"',
        ')"',
    ]
    lexer = streamingjson.Lexer()

    for json_fragment in arguments:
        try:
            lexer.append_string(json_fragment)
            print(lexer.complete_json())
        except ValueError as e:
            print(f"invalied json string appended: {e}")


# will print:
# {"fu":null}
# {"function":null}
# {"function_name":null}
# {"function_name":null}
# {"function_name":null}
# {"function_name":"run"}
# {"function_name":"run_code"}
# {"function_name":"run_code"}
# {"function_name":"run_code", "argu":null}
# {"function_name":"run_code", "arguments":null}
# {"function_name":"run_code", "arguments":null}
# {"function_name":"run_code", "arguments": "print("}
# {"function_name":"run_code", "arguments": "print(\"hello"}
# {"function_name":"run_code", "arguments": "print(\"hello world"}
# {"function_name":"run_code", "arguments": "print(\"hello world\""}
# {"function_name":"run_code", "arguments": "print(\"hello world\")"}


if __name__ == "__main__":
    main()
