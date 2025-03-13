# Project Disco

Disco uses resource objects like volumes, models, and tokenizers to construct AI pipelines via composing stages.

```python
# todo
```

## Development

You can do `pytest -s -k <pattern>` to run a script and it will handle imports.

```python
make venv   # source ./venv/activate
make check  # run pre-commit lints
make test   # run unit tests
```

## Situation

- We load heterogenous data sources such as..
  - structured parquet and csv
  - semi-structured html, json, and semantic trees (see **Ideas**)
  - unstructured raw text
- Our team has common resources and services like..
  - Volumes
  - Models & Tokenizers
  - LSPs
  - Validators (i.e. JSON schema)

## Problem

Our routine jobs are built with one-off code that is often copy-pasted from previous jobs. This code has many a lot of magic strings and hardcoded paths which work well for the current state of things, however these jobs require our resources and services (volumes, models, LSPs) to remain unchanged else we have to update these hardcoded paths. This ultimately makes job maintenance difficult and we want to interface with our resources like we interact with our tables in our lakehouse.

## Links

- https://github.com/rchowell/Disco
- https://github.com/openai/tiktoken

## Ideas

- I like the idea of creating a code “semantic tree” by sending code to an LSP and getting back a detailed JSON tree with as much information as possible.

- pipelining of various objects on a dataset

```py
class MyValidator():
    name = "my_validator"
    ...
class MyTokenizer():
    name = "my_tokenizer"
    ...
class MyModel():
    name = "my_model"
    ...


disco.read("pond://yellow.parquet").pipeline(["my_validator", "my_tokenizer", "my_model"])
```

## Issues/Feature Requests

### Feature Requests

- we don't actually have a way to read in a text file, see https://github.com/Eventual-Inc/Daft/issues/2859
- having `with_column` but prepend the column
- support "gz" as a gzip codec alias

### Enhancements

- `tokenize_encode` and `tokenize_decode` docs are not that great. I think adding some method overloading would help clean them up a bit.
- `tokenize_encode` should return a fixedsizelist instead of a list.
