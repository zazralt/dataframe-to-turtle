# dataframe-to-turtle

**dataframe-to-turtle** is a lightweight Python utility for converting `pandas.DataFrame` objects into [RDF](https://www.w3.org/RDF/) serialized in [Turtle](https://www.w3.org/TR/turtle/) format. It allows you to define custom mappings for prefixes, RDF classes, predicates, datatypes, language tags, and object relations—enabling seamless transformation of tabular data into Linked Data.

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
    "subject": {
        "prefix": "ex",
        "column": "name",
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
@prefix ex: <http://example.com/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Alice a foaf:Person ;
    foaf:name "Alice"@en ;
    schema:age "30"^^xsd:integer ;
    foaf:knows ex:Bob .

ex:Bob a foaf:Person ;
    foaf:name "Bob"@en ;
    schema:age "25"^^xsd:integer ;
    foaf:knows ex:Alice .
```

---

# Converting CSV or Excel Files to Turtle

You can use the `convert_file_to_turtle` function to read tabular data from a CSV or Excel file, convert it to RDF Turtle, and write the result to a `.ttl` file.

## Function Signature

```python
convert_file_to_turtle(input_path: str, config: dict, output_path: str, index_col: str = None) -> None
````

## Parameters

* **`input_path`**: Path to the source `.csv`, `.xls`, or `.xlsx` file.
* **`config`**: RDF mapping configuration (same structure as for `convert_dataframe_to_turtle`).
* **`output_path`**: Destination file path for Turtle output.

## Example

```python
from dataframe_to_turtle import convert_dataframe_to_turtle, convert_file_to_turtle

convert_file_to_turtle(
    input_path="data/people.xlsx",
    config=my_rdf_config,
    output_path="output/people.ttl",
)
```

If `index_col` is not specified, the function will use the default DataFrame index.
