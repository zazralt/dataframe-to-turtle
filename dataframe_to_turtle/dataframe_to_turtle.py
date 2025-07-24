import pandas as pd
import os

import pandas as pd

def convert_dataframe_to_turtle(dataframe: pd.DataFrame, config: dict) -> str:
    """
    Converts a pandas DataFrame into RDF Turtle format using a human-readable config structure.
    
    Parameters:
        dataframe (pd.DataFrame): The input DataFrame to serialize.
        config (dict): The RDF mapping configuration with the following structure:
            {
                "prefixes": { "prefix": "uri", ... },
                "subjects": {
                    "column": "index_column_name",  # optional, if not provided, the index will be used
                    "prefix": "prefix",
                    "classes": ["prefix1:class1", "prefix2:class2"]
                },
                "mappings": [
                    {
                        "column": "column_name",
                        "predicate": "prefix1:property1",
                        "prefix": "object_prefix" # mandatory for relations
                        "language": "en",         # optional
                        "data_type": "xsd:type",  # optional
                    },
                    ...
                ]
            }

    Returns:
        str: RDF Turtle serialization of the DataFrame.
    """
    prefixes = config["prefixes"]
    subject_index = config["subjects"]["column"]
    subject_prefix = config["subjects"]["prefix"]
    subject_classes = config["subjects"]["classes"]
    mappings_list = config["mappings"]

    # Pre-index column mappings for fast access
    valid_column_names = [m["column"] for m in mappings_list if m["column"] in dataframe.columns]
    mapping_index = {m["column"]: m for m in mappings_list if m["column"] in dataframe.columns}
    missing = [m["column"] for m in mappings_list if m["column"] not in dataframe.columns]
    if missing:
        print(f"Warning: the following columns in config were not found in the DataFrame: {missing}")

    # Set index from a column and leave column in df
    if subject_index:
        if subject_index not in dataframe.columns:
            raise ValueError(f"Index column '{subject_index}' not found in dataframe.")
        df.index = df[subject_index]
    
    lines = []

    # Write prefixes
    for prefix, uri in prefixes.items():
        lines.append(f"@prefix {prefix}: <{uri}> .")
    lines.append("")  # Blank line

    # Write triples
    for subject_id, row in dataframe.iterrows():
        subject_str = f"{subject_prefix}:{subject_id}"
        lines.append(f"{subject_str} a {', '.join(subject_classes)} ;")

        predicate_lines = []

        for column_name in valid_column_names:
            mapping = mapping_index[column_name]
            predicate_str = mapping["predicate"]
            value = row[column_name]

            if pd.isna(value):
                continue

            # Format object
            if "prefix" in mapping:
                object_prefix = mapping["prefix"]
                object_id = str(value).replace(' ', '')
                object_str = f"{object_prefix}:{object_id}"
            elif "language" in mapping:
                language_tag = mapping["language"]
                object_str = f"\"{value}\"@{language_tag}"
            elif "data_type" in mapping:
                dt = mapping["data_type"]
                object_str = f"\"{value}\"^^{dt}"
            else:
                if isinstance(value, (int, float)):
                    object_str = str(int(value))
                else:
                    object_str = f"\"{value.replace('"', '\\"')}\""

            predicate_lines.append(f"    {predicate_str} {object_str}")

        # End statement: last predicate with dot
        for i, triple in enumerate(predicate_lines):
            end = " ." if i == len(predicate_lines) - 1 else " ;"
            lines.append(triple + end)

        if not predicate_lines:
            lines[-1] = lines[-1][:-1] + " ."  # Fix trailing semicolon if no predicates

        lines.append("")  # Blank line between subjects

    return "\n".join(lines)

def convert_file_to_turtle(input_path: str, config: dict, output_path: str) -> None:
    """
    Reads a CSV or Excel file, converts it to RDF Turtle format using the provided configuration,
    and writes the result to a .ttl file.

    Parameters:
        input_path (str): 
            Path to the input tabular file (.csv, .xls, or .xlsx).
        config (dict): 
            RDF mapping configuration compatible with convert_dataframe_to_turtle.
        output_path (str): 
            Path to the output .ttl file.

    Raises:
        ValueError: If the file extension is unsupported.
        FileNotFoundError: If the input file does not exist.
    """
    ext = os.path.splitext(input_path)[1].lower()

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if ext == ".csv":
        df = pd.read_csv(input_path)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(input_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    turtle_str = convert_dataframe_to_turtle(df, config)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(turtle_str)
