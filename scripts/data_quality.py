def check_duplicates(df, columns):
    duplicates = df[df.duplicated(subset=columns)]
    return duplicates

def check_nulls(df, columns):
    null_rows = df[df[columns].isnull().any(axis=1)]
    return null_rows

def check_range(df, column, min_val, max_val):
    invalid = df[
        (df[column] < min_val) |
        (df[column] > max_val)
    ]
    return invalid