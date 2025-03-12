# Project Disco

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
 