import pandas as pd

def convert_dataframe_to_turtle(dataframe: pd.DataFrame, config: dict) -> str:
    """
    Converts a pandas DataFrame into a Turtle (TTL) serialization string for RDF data.

    Each row in the DataFrame is treated as an RDF subject, with the column values mapped
    to predicates and objects based on the provided configuration. The function supports
    custom prefixes, datatype declarations, language tags, and object relations.

    Parameters:
        dataframe (pd.DataFrame): 
            A DataFrame where each row represents an RDF subject and each column represents 
            a potential predicate. The DataFrame index will be used to construct subject URIs.

        config (dict): 
            A dictionary specifying the RDF mapping configuration with the following keys:
            
            - "prefixes" (dict): 
                Maps prefix labels to full URI namespaces. Used to declare `@prefix` headers.
            - "subject_prefix" (str): 
                The prefix to be used when constructing subject URIs.
            - "subject_classes" (list of str): 
                RDF classes to assign to each subject using `a`.
            - "predicate_maps" (dict): 
                Maps DataFrame column names to RDF predicates.
            - "language_tags" (optional dict): 
                Maps column names to language tags (e.g., "en") for literal values.
            - "data_types" (optional dict): 
                Maps column names to datatype URIs (e.g., "xsd:integer").
            - "relations" (optional list): 
                Column names to treat as object references (not quoted literals).

    Returns:
        str: 
            A string containing the Turtle serialization of the input DataFrame based on the
            given configuration.

    Example:
        >>> data = {"name": ["Alice"], "age": [30], "knows": ["foaf:Bob"]}
        >>> df = pd.DataFrame(data, index=["Alice"])
        >>> config = {
        ...     "prefixes": {"foaf": "http://xmlns.com/foaf/0.1/", "xsd": "http://www.w3.org/2001/XMLSchema#"},
        ...     "subject_prefix": "foaf",
        ...     "subject_classes": ["foaf:Person"],
        ...     "predicate_maps": {"name": "foaf:name", "age": "foaf:age", "knows": "foaf:knows"},
        ...     "language_tags": {"name": "en"},
        ...     "data_types": {"age": "xsd:integer"},
        ...     "relations": ["knows"]
        ... }
        >>> convert_dataframe_to_turtle(df, config)
        '@prefix foaf: <http://xmlns.com/foaf/0.1/> .\\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\\n...'

    Notes:
        - Columns not specified in `predicate_maps` are ignored.
        - Missing (NaN) values in the DataFrame are skipped.
        - The function assumes all subject identifiers are unique (i.e., row indices are unique).
    """

    # Extract parameters from config
    prefixes = config["prefixes"]
    subject_prefix = config["subject_prefix"]
    subject_classes = config["subject_classes"]
    predicate_maps = config["predicate_maps"]
    language_tags = config.get("language_tags", {})
    data_types = config.get("data_types", {})
    relations = set(config.get("relations", []))

    lines = []

    # Write prefix declarations
    for prefix, uri in prefixes.items():
        lines.append(f"@prefix {prefix}: <{uri}> .")
    lines.append("")  # Empty line after prefixes

    # Iterate through each row (subject)
    for subject_id, row in dataframe.iterrows():
        subject_uri = f"{subject_prefix}:{subject_id}"
        lines.append(f"{subject_uri} a {', '.join(subject_classes)} ;")

        column_names = list(dataframe.columns)
        predicate_lines = []

        for column_index, column_name in enumerate(column_names):
            if column_name not in predicate_maps:
                continue

            predicate = predicate_maps[column_name]
            value = row[column_name]
            if isinstance(value, (str)):
                value = value.replace('"', '\\"')

            if pd.isna(value):
                continue  # Skip missing values

            # Format the object
            if column_name in relations:
                object_str = value.replace(' ', '')
            elif column_name in language_tags:
                lang = language_tags[column_name]
                object_str = f"\"{value}\"@{lang}"
            elif column_name in data_types:
                datatype = data_types[column_name]
                object_str = f"\"{value}\"^^{datatype}"
            else:
                if isinstance(value, (int, float)):
                    object_str = f"{value}"
                else:
                    object_str = f"\"{value}\""

            predicate_lines.append(f"    {predicate} {object_str}")

        # Write predicates with semicolon, end last with dot
        for i, line in enumerate(predicate_lines):
            end = " ." if i == len(predicate_lines) - 1 else " ;"
            lines.append(line + end)

        if not predicate_lines:
            lines[-1] = lines[-1][:-1] + " ."  # Change trailing ";" to "."

        lines.append("")  # Separate subjects with a blank line

    return "\n".join(lines)
