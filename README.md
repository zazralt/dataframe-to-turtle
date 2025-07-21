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
pip install git+https://github.com/zazralt/dataframe-to-turtle.git
````

---

## Usage

```python
import pandas as pd
from dataframe_to_turtle import convert_dataframe_to_turtle

data = {
    "name": ["Alice", "Bob"],
    "age": [30, 25],
    "knows": ["Bob", "Alice"]
}
df = pd.DataFrame(data, index=["Alice", "Bob"])

config = {
    "prefixes": {
        "ex": "http://example.com/",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "schema": "http://schema.org/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    "subjects": {
        "prefix": "ex",
        "classes": ["foaf:Person"]
    },
    "mappings": [
        {
            "column": "name",
            "predicate": "foaf:name",
            "language": "en"
        },
        {
            "column": "age",
            "predicate": "schema:age",
            "data_type": "xsd:integer"
        },
        {
            "column": "knows",
            "predicate": "foaf:knows",
            "prefix": "ex"
        }
    ]
}

ttl_output = convert_dataframe_to_turtle(df, config)
print(ttl_output)
```

---

## Output Example

```turtle
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

foaf:Alice a foaf:Person ;
    foaf:name "Alice"@en ;
    schema:age "30"^^xsd:integer ;
    foaf:knows foaf:Bob .

foaf:Bob a foaf:Person ;
    foaf:name "Bob"@en ;
    schema:age "25"^^xsd:integer ;
    foaf:knows foaf:Alice .
```

---

## Configuration Reference

| Key               | Type              | Description                                           |
| ----------------- | ----------------- | ----------------------------------------------------- |
| `prefixes`        | `dict`            | Mapping of prefix labels to URIs                      |
| `subject_prefix`  | `str`             | Prefix to use for subject URIs                        |
| `subject_classes` | `list[str]`       | RDF classes for each subject                          |
| `predicate_maps`  | `dict`            | Maps DataFrame columns to RDF predicates              |
| `language_tags`   | `dict` (optional) | Assigns language tags to literal values               |
| `data_types`      | `dict` (optional) | Explicit datatype URIs for column values              |
| `relations`       | `list` (optional) | Columns treated as URI references instead of literals |


Here is a short `README.md` add-on section describing the `convert_file_to_turtle` function and how to use it:

---

## Converting CSV or Excel Files to Turtle

You can use the `convert_file_to_turtle` function to read tabular data from a CSV or Excel file, convert it to RDF Turtle, and write the result to a `.ttl` file.

### Function Signature

```python
convert_file_to_turtle(input_path: str, config: dict, output_path: str, index_col: str = None) -> None
````

### Parameters

* **`input_path`**: Path to the source `.csv`, `.xls`, or `.xlsx` file.
* **`config`**: RDF mapping configuration (same structure as for `convert_dataframe_to_turtle`).
* **`output_path`**: Destination file path for Turtle output.
* **`index_col`** *(optional)*: Name or integer index of the column to use as the RDF subject identifier.

### Example

```python
from dataframe_to_turtle import convert_dataframe_to_turtle, convert_file_to_turtle

convert_file_to_turtle(
    input_path="data/people.xlsx",
    config=my_rdf_config,
    output_path="output/people.ttl",
    index_col="person_id"
)
```

If `index_col` is not specified, the function will use the default DataFrame index.
