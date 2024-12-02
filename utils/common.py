import numpy as np
import pandas as pd


def safe_format_value(value):
    if pd.isna(value):
        return 'N/A'
    elif isinstance(value, (float, np.float64)):
        return f"{value:.2f}"
    return str(value)
