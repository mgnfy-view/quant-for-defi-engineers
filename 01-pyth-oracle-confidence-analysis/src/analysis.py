"""
Analysis module for detecting confidence breaches and calculating correlations
"""

import pandas as pd
import numpy as np
from config import TIMESTAMP_COL, PRICE_COL, CONF_COL, RETURNS_COL
from constants import PERCENTAGE_BASE


def calculate_returns(df):
    """
    Calculate price returns (percentage change)

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with price column

    Returns:
    --------
    pandas.DataFrame
        DataFrame with added "priceReturns" column
    """

    df[RETURNS_COL] = df[PRICE_COL].pct_change() * PERCENTAGE_BASE

    print(f"Calculated price returns for {len(df)} records")

    return df


def detect_breaches(df, threshold_bps):
    """
    Detect confidence breaches above threshold

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with confidence_bps column
    threshold_bps : float, optional
        Confidence threshold in basis points (uses config if None)

    Returns:
    --------
    pandas.DataFrame
        DataFrame containing only breach records
    """

    breaches = df[df[CONF_COL] > threshold_bps].copy()

    print("\nBreach Detection Results:")
    print(f"  Threshold: {threshold_bps} bps")
    print(f"  Total records: {len(df)}")
    print(f"  Breaches found: {len(breaches)}")
    print(f"  Breach rate: {len(breaches) / len(df) * 100:.2f}%")

    if len(breaches) > 0:
        print("  Confidence at breaches:")
        print(f"    Mean: {breaches[CONF_COL].mean():.2f} bps")
        print(f"    Max: {breaches[CONF_COL].max():.2f} bps")
        print(f"    Min: {breaches[CONF_COL].min():.2f} bps")

    return breaches


def extract_previous_returns(df, breach_indices, lookback_periods):
    """
    Extract previous returns for each breach

    Parameters:
    -----------
    df : pandas.DataFrame
        Full DataFrame with returns column
    breach_indices : array-like
        Indices of breach events
    lookback_periods : int, optional
        Number of periods to look back (uses config if None)

    Returns:
    --------
    pandas.DataFrame
        DataFrame with breach info and previous return features
    """

    breach_data = []

    for idx in breach_indices:
        # Skip if not enough history
        if idx < lookback_periods:
            continue

        # Get previous returns
        start_idx = idx - lookback_periods
        end_idx = idx
        previous_returns = df.loc[start_idx : end_idx - 1, RETURNS_COL].values

        # Skip if any NaN values
        if np.isnan(previous_returns).any():
            continue

        # Calculate features
        breach_info = {
            "breachIndex": idx,
            "breachTime": df.loc[idx, TIMESTAMP_COL],
            "confidenceAtBreach": df.loc[idx, CONF_COL],
            "priceAtBreach": df.loc[idx, PRICE_COL],
            "meanReturn": np.mean(previous_returns),
            "volatility": np.std(previous_returns),
            "cumulativeReturn": np.sum(previous_returns),
            "maxReturn": np.max(previous_returns),
            "minReturn": np.min(previous_returns),
            "absMeanReturn": np.mean(np.abs(previous_returns)),
        }

        breach_data.append(breach_info)

    breach_df = pd.DataFrame(breach_data)

    print(f"\nExtracted previous returns for {len(breach_df)} breaches")
    print(f"Lookback period: {lookback_periods} periods")

    return breach_df


def calculate_correlations(breach_df, method):
    """
    Calculate correlations between return features and confidence

    Parameters:
    -----------
    breach_df : pandas.DataFrame
        DataFrame with breach info and return features
    method : str, optional
        Correlation method: 'pearson', 'spearman', or 'kendall'
        (uses config if None)

    Returns:
    --------
    dict
        Dictionary of correlation coefficients
    """

    if len(breach_df) < 2:
        print("Not enough breaches to calculate correlations")
        return {}

    # Calculate correlations for each feature
    features = [
        "meanReturn",
        "volatility",
        "cumulativeReturn",
        "maxReturn",
        "minReturn",
        "absMeanReturn",
    ]

    correlations = {}

    for feature in features:
        corr = breach_df["confidenceAtBreach"].corr(breach_df[feature], method=method)
        correlations[feature] = corr

    print(f"\n{method.capitalize()} Correlation Results:")
    print("=" * 60)
    for feature, corr in correlations.items():
        interpretation = interpret_correlation(corr)
        print(f"  {feature:20s}: {corr:+.4f}  ({interpretation})")
    print("=" * 60)

    return correlations


def interpret_correlation(corr):
    """
    Interpret correlation coefficient strength

    Parameters:
    -----------
    corr : float
        Correlation coefficient

    Returns:
    --------
    str
        Human-readable interpretation
    """
    abs_corr = abs(corr)

    if abs_corr >= 0.7:
        strength = "Strong"
    elif abs_corr >= 0.4:
        strength = "Moderate"
    elif abs_corr >= 0.2:
        strength = "Weak"
    else:
        strength = "Very weak"

    direction = "positive" if corr > 0 else "negative"

    return f"{strength} {direction}"
