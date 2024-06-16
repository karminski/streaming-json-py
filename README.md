# streaming-json-py


Welcome to **streaming-json-py**, a groundbreaking library designed to revolutionize the way we handle stream JSON parsing.  

In an era dominated by LLMs (Large Language Models), the ability to efficiently parse JSON streams is more critical than ever. Traditionally, JSON parsing libraries have fallen short, requiring JSON data to be fully generated before any parsing can begin. streaming-json-py challenges this limitation head-on.

### Key Features

- **Real-Time JSON Parsing**: With streaming-json-py, you no longer need to wait for the entire JSON data to be generated. This library allows for the parsing of JSON as it is being streamed (this means JSON stream can stops at any position), significantly cutting down the time-to-first-token.
- **Seamless Integration**: Designed to complement existing JSON parsing libraries, streaming-json-py preprocesses incomplete JSON strings, transforming them into valid, parseable JSON. This means you can continue using your preferred JSON library with our tool seamlessly.
- **Enhanced User Experience**: By enabling real-time data processing, our library drastically reduces the wait time for end-users. Display JSON structures to users without the delay typically associated with complete JSON generation.

### Example Usage

Basically, this library is used to complete fragmented JSON, making it into syntactically correct JSON. For example:

```{"a":``` will complete to ```{"a":null}```

and When the JSON stream continues to output as:

```{"a":[tr``` will complete to ```{"a":[true]}```

Do not worry about the JSON stream stopping anywhere, such as at a comma:

```{"a":[true],``` will complete to ```{"a":[true]}```

Escaped characters? No problem:  

```{"a":[true], "b": "this is unicode \u54"``` will complete to ```{"a":[true], "b": "this is unicode "}``` 

(After the stream outputs the complete Unicode, it will then display.)


**Here’s a quick example to get you started:**


For more examples please see: [examples](./examples/)

### Benchmarks


### License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
