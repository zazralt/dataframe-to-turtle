````markdown
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
````

Install dependencies:

```bash
pip install pandas
```

---

## Usage

```python
import pandas as pd
from dataframe_to_turtle import convert_dataframe_to_turtle

data = {
    "name": ["Alice", "Bob"],
    "age": [30, 25],
    "knows": ["foaf:Bob", "foaf:Alice"]
}
df = pd.DataFrame(data, index=["Alice", "Bob"])

config = {
    "prefixes": {
        "foaf": "http://xmlns.com/foaf/0.1/",
        "schema": "http://schema.org/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    "subject_prefix": "foaf",
    "subject_classes": ["foaf:Person"],
    "predicate_maps": {
        "name": "foaf:name",
        "age": "schema:age",
        "knows": "foaf:knows"
    },
    "language_tags": {
        "name": "en"
    },
    "data_types": {
        "age": "xsd:integer"
    },
    "relations": ["knows"]
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
    schema:age 30 ;
    foaf:knows foaf:Bob .

foaf:Bob a foaf:Person ;
    foaf:name "Bob"@en ;
    schema:age 25 ;
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

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---
