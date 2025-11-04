"""
Data loading and preprocessing module
"""

import pandas as pd
from constants import BASIS_POINTS
from config import TIMESTAMP_COL, PRICE_COL, CONF_COL, CONF_VAR_COL


def load_pyth_data(file_path):
    """
    Load Pyth price data from CSV

    Parameters:
    -----------
    file_path : str
        Path to the CSV file

    Returns:
    --------
    pandas.DataFrame
        Loaded and parsed data
    """

    df = pd.read_csv(file_path)

    print(f"Loaded {len(df)} records")
    print(f"Time range: {df[TIMESTAMP_COL].min()} to {df[TIMESTAMP_COL].max()}")

    return df


def process_loaded_data(df):
    """
    Process loaded data: retain only required columns, sort by time, and convert confidence into basis points

    Parameters:
    -----------
    df : pandas.DataFrame
        Raw loaded DataFrame

    Returns:
    --------
    pandas.DataFrame
        Processed DataFrame with only timestamp, price, and confidence columns
    """

    # Select only required columns
    df_processed = df[[TIMESTAMP_COL, PRICE_COL, CONF_COL]].copy()

    # Convert timestamp to UNIX timestamp
    df[TIMESTAMP_COL] = pd.to_datetime(df[TIMESTAMP_COL])
    df[TIMESTAMP_COL] = df[TIMESTAMP_COL].astype("int64") // 10**9

    # Sort by timestamp
    df_processed = df_processed.sort_values(TIMESTAMP_COL).reset_index(drop=True)

    # Convert confidence values into basis points
    df_processed[CONF_COL] = df_processed[CONF_COL] * BASIS_POINTS

    print(
        f"Processed data: {len(df_processed)} records with {len(df_processed.columns)} columns"
    )

    return df_processed


def downsize_processed_data(df, target_size, window_size):
    """
    Downsize the processed data by selecting windows with maximum variance in confidence
    This preserves interesting periods with high volatility

    Parameters:
    -----------
    df : pandas.DataFrame
        Processed DataFrame to downsize
    target_size : int, optional
        Approximate target number of records (default: 20000)
    window_size : int, optional
        Size of rolling window to calculate variance (default: 100)

    Returns:
    --------
    pandas.DataFrame
        Downsized DataFrame with high-variance periods preserved
    """

    # Calculate rolling variance of confidence
    df[CONF_VAR_COL] = df[CONF_COL].rolling(window=window_size, center=True).var()

    # Fill NaN values at the edges with 0
    df[CONF_VAR_COL] = df[CONF_VAR_COL].fillna(0)

    # Calculate how many windows we need to select
    num_windows = target_size // window_size

    # Divide dataframe into chunks
    chunk_size = len(df) // num_windows

    selected_indices = []

    for i in range(num_windows):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, len(df))

        if start_idx >= len(df):
            break

        chunk = df.iloc[start_idx:end_idx]

        # Find the index with maximum variance in this chunk
        if len(chunk) > 0:
            max_var_idx = chunk[CONF_VAR_COL].idxmax()

            # Select a window around the maximum variance point
            window_start = max(0, max_var_idx - window_size // 2)
            window_end = min(len(df), max_var_idx + window_size // 2)

            selected_indices.extend(range(window_start, window_end))

    # Remove duplicates and sort
    selected_indices = sorted(set(selected_indices))

    # Select the data
    df_downsized = df.iloc[selected_indices].copy()

    # Drop the variance column as it's no longer needed
    df_downsized.drop(CONF_VAR_COL, axis=1, inplace=True)

    print(
        f"Downsized data using variance sampling: {len(df)} → {len(df_downsized)} records"
    )
    print(
        f"Preserved high-variance periods representing {len(df_downsized) / len(df) * 100:.2f}% of data"
    )

    return df_downsized
