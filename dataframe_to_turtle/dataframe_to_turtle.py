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
                    "prefix": "prefix",
                    "classes": ["prfx:class1", "prfx:class2"]
                },
                "mappings": [
                    {
                        "column": "column_name",
                        "predicate": "prfx:property1",
                        "language": "en",        # optional
                        "datatype": "xsd:type",  # optional
                        "type": "relation"       # optional ("relation" = treat value as URI)
                    },
                    ...
                ]
            }

    Returns:
        str: RDF Turtle serialization of the DataFrame.
    """
    prefixes = config["prefixes"]
    subject_prefix = config["subjects"]["prefix"]
    subject_classes = config["subjects"]["classes"]
    mappings_list = config["mappings"]

    # Pre-index column mappings for fast access
    valid_column_names = [m["column"] for m in mappings_list if m["column"] in dataframe.columns]
    mapping_index = {m["column"]: m for m in mappings_list if m["column"] in dataframe.columns}
    missing = {m["column"]: m for m in mappings_list if m["column"] not in dataframe.columns}
    if missing:
        print(f"Warning: the following columns in config were not found in the DataFrame: {missing}")

    lines = []

    # Write prefixes
    for prefix, uri in prefixes.items():
        lines.append(f"@prefix {prefix}: <{uri}> .")
    lines.append("")  # Blank line

    for subject_id, row in dataframe.iterrows():
        subject_uri = f"{subject_prefix}:{subject_id}"
        lines.append(f"{subject_uri} a {', '.join(subject_classes)} ;")

        predicate_lines = []

        for column_name in valid_column_names:
            mapping = mapping_index[column_name]
            predicate = mapping["predicate"]
            value = row[column_name]

            if pd.isna(value):
                continue

            # Format object
            if mapping.get("type") == "relation":
                object_str = str(value).replace('"', '\\"')
            elif "language" in mapping:
                lang = mapping["language"]
                object_str = f"\"{value}\"@{lang}"
            elif "datatype" in mapping:
                dt = mapping["datatype"]
                object_str = f"\"{value}\"^^{dt}"
            else:
                if isinstance(value, (int, float)):
                    object_str = str(int(value))
                else:
                    object_str = f"\"{value}\""

            predicate_lines.append(f"    {predicate} {object_str}")

        # End statement: last predicate with dot
        for i, triple in enumerate(predicate_lines):
            end = " ." if i == len(predicate_lines) - 1 else " ;"
            lines.append(triple + end)

        if not predicate_lines:
            lines[-1] = lines[-1][:-1] + " ."  # Fix trailing semicolon if no predicates

        lines.append("")  # Blank line between subjects

    return "\n".join(lines)

def convert_file_to_turtle(input_path: str, config: dict, output_path: str, index_col: str = None) -> None:
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
        index_col (str, optional): 
            Name or index of the column to use as the DataFrame index (subject ID). 
            If None, the default index will be used.

    Raises:
        ValueError: If the file extension is unsupported.
        FileNotFoundError: If the input file does not exist.
    """
    ext = os.path.splitext(input_path)[1].lower()

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if ext == ".csv":
        df = pd.read_csv(input_path, index_col=index_col)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(input_path, index_col=index_col)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    turtle_str = convert_dataframe_to_turtle(df, config)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(turtle_str)
