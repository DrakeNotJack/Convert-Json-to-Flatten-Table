import pandas as pd
from pandas import json_normalize
import copy

data = [
    {
        "A": {
            "B": {
                "C": 1,
                "D": {
                    "E": 2,
                    "F": {"G": 5, "L":"Great","M":[{"N":"List1"},{"N":"List2"}]}
                }
            }
        },
        "H": [{"I": 6}, {"I": 7}, {"I": 8}],
        "J": {"K": 9}
    },
    {
        "A": {
            "B": {
                "C": 10,
                "D": {
                    "E": 11,
                    "F": {"G": 14, "L":"No Great", "M":[{"N":"Dict1"},{"N":"Dict12"}]}
                }
            }
        },
        "H": [{"I": 15}, {"I": 16}, {"I": 17}],
        "J": {"K": 18}
    }
]


# Function to normalize the flattened data
def normalize_flattened_data(flattened_data):
    # Normalize the flattened JSON data into a DataFrame
    df = json_normalize(flattened_data)
    
    # Identify columns with list elements and expand them
    def expand_lists(df):
        list_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, list)).any()]
        for col in list_columns:
            df = df.explode(col).reset_index(drop=True)
            nested_cols = df[col].dropna().apply(lambda x: isinstance(x, dict)).any()
            if nested_cols:
                expanded_cols = json_normalize(df[col].dropna().tolist()).add_prefix(col + '.')
                df = df.drop(columns=[col]).join(expanded_cols)
        return df

    # Expand lists in the DataFrame
    df = expand_lists(df)

    return df

# Normalize the flattened data
df = normalize_flattened_data(data)

df
