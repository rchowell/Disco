# Project Disco

It's a party, and we only play daft.

## Example

Disco uses resource objects like volumes, models, and tokenizers to construct AI pipelines via composing stages.

```python
# todo
```

## Background

This project was intended to position ourselves as the customer and push our tools to be better.

**Customer Situation**

- We load heterogenous data sources such as..
  - structured parquet and csv
  - semi-structured html, json, and semantic trees (see **Ideas**)
  - unstructured raw text
- Our team has common resources and services like..
  - Volumes ... like S3 buckets
  - Tables ... like Iceberg & DeltaLake
  - Models & Tokenizers
  - LSPs
  - Validators .. like JSONSchema & Pydantic

**Customer Problem**

Using these resources together requires many libraries an stitching things together with one-off code.

    Our routine jobs are built with one-off code that is often copy-pasted from previous jobs. This code has many magic strings and hardcoded paths which work well for the current state of things, however these jobs require our resources and services (volumes, models, LSPs) to remain unchanged else we have to update these hardcoded paths. This ultimately makes job maintenance difficult and we want to interface with our resources like we interact with our tables in our lakehouse. - Customer

**Customer Ask**

> *We want to interface with our resources like we interact with our tables in our lakehouse*

## Development

You can do `pytest -s -k <pattern>` to run a script and it will handle imports.

```shell
make venv   # source ./venv/activate
make check  # run pre-commit lints
make test   # run unit tests
```

## Examples

To run the examples, ensure the venv is activated.

```shell
uv pip install -e .
python ./examples/text_stream_example.py
```

## Disco Ideas

- make streams lazy and flatten, the problem is I want to read a bunch of gzipped files into a daft DataFrame using existing daft operators.
- flatten streams to dataframes with concat
- rename catalog to context or something
- I like the idea of creating a code “semantic tree” by sending code to an LSP and getting back a detailed JSON tree with as much information as possible.
- pipelining of various objects on a dataset
- chunk a stream to be sent to an LLM in reasonable sizes

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

## Daft Requests

- we don't actually have a way to read in a text file, see https://github.com/Eventual-Inc/Daft/issues/2859
- having `with_column` but prepend the column -- +1
- support "gz" as a gzip codec alias
- support reading things like `.csv.gz` or `.json.zstd`
- `tokenize_encode` and `tokenize_decode` docs are not that great. I think adding some method overloading would help clean them up a bit.
- `tokenize_encode` should return a fixedsizelist instead of a list.
- produce an output stream from a dataframe e.g. csv output stream
- multi-column projections
- why doesn't `col("a")["field"]` work?
- produce a dataframe, where each line is an entry, from compressed logs is a bit difficult
- count uses the name of the argument which means I'm forced to alias it. `Due to: DaftError::ValueError Attempting to make a Schema with duplicate field names: url`
- running a classifier on a column is painfully slow and unintuitive via udfs. It'd be nice to have a way to natively run classifiers.
- from a json column, there is no easy way to extract that in to a specified datatype. (polars has `.json_extract`)
- read_text and read_blob functions
- column selectors would be huge. for example when expanding a struct field, there's no way to do `select(col("struct").struct.get("*"), col("*", exclude=["struct"]))`
- meta functions on exprs, such as getting fields from `struct` 
