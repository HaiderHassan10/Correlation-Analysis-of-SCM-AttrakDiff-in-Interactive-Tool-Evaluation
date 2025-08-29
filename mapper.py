import pandas as pd

def get_attrakdiff_mappings():
    mappings = {}
    pairs = {
        'impractical - practical': ('impractical', 'practical'),
        'complicated - simple': ('complicated', 'simple'),
        'dull - creative': ('dull', 'creative'),
        'boring - exciting': ('boring', 'exciting'),
        'tacky - stylish': ('tacky', 'stylish'),
        'amateurish - professional': ('amateurish', 'professional'),
        'unpleasant - pleasant': ('unpleasant', 'pleasant'),
        'unattractive - attractive': ('unattractive', 'attractive'),
    }

    for col, (neg, pos) in pairs.items():
        mappings[col] = {
            pos: 2,
            f'quite {pos}': 1,
            f'somewhat {pos}': 1,
            'neutral': 0,
            f'somewhat {neg}': -1,
            f'quite {neg}': -1,
            neg: -2,
            # Typos found in data
            f'somwhat {pos}': 1,
            f'qute {pos}': 1,
            f'somwhat {neg}': -1,
            f'qute {neg}': -1,
            'somewhat impratical': -1,
        }
    return mappings

def get_scm_mapping():
    """
    Returns a mapping for SCM data.
    Note: The values in SCM data seem to correspond to a 4-point scale.
    We are mapping them to 2, 1, 0, -1.
    """
    return {
        'highly applicable': 2,
        'applicable': 1,
        'neutral': 0,
        'does not apply': -1,
        'not applicable': -1, # handle variations
    }

def map_attrakdiff_df(df):
    mappings = get_attrakdiff_mappings()
    df_mapped = df.copy()
    for col, mapping in mappings.items():
        if col in df_mapped.columns:
            # First strip whitespace from all cells and convert to lower case
            df_mapped[col] = df_mapped[col].str.strip().str.lower()
            df_mapped[col] = df_mapped[col].map(mapping)
    return df_mapped

def map_scm_df(df):
    mapping = get_scm_mapping()
    df_mapped = df.copy()
    for col in df_mapped.columns:
        # First strip whitespace from all cells and convert to lower case
        df_mapped[col] = df_mapped[col].str.strip().str.lower()
        df_mapped[col] = df_mapped[col].map(mapping)
    return df_mapped
