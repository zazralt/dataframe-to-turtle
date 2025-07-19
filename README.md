# dataframe-to-turtle

**dataframe-to-turtle** is a lightweight Python utility for converting `pandas.DataFrame` objects into [RDF](https://www.w3.org/RDF/) serialized in [Turtle](https://www.w3.org/TR/turtle/) format. It allows you to define custom mappings for prefixes, RDF classes, predicates, datatypes, language tags, and object relations—enabling seamless transformation of tabular data into Linked Data.

## Features

- Convert DataFrames into RDF Turtle serialization
- Supports RDF class and predicate mapping
- Handles language-tagged literals
- Supports explicit datatype annotations (e.g., `xsd:integer`)
- Generates semantic object references for relations
- Configurable prefix declarations

---

## Installation

This package is currently not available on PyPI. To use it directly:

```bash
git clone https://github.com/your-org/dataframe-to-turtle.git
cd dataframe-to-turtle
