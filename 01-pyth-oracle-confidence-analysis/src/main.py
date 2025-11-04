"""
Main script to run Pyth oracle confidence analysis
"""

from config import (
    INPUT_CSV_PATH,
    PLOT_OUTPUT_DIR,
    CONFIDENCE_THRESHOLD_BPS,
    RETURN_LOOKBACK_PERIODS,
    CORRELATION_METHOD,
)
from load_and_process_data import (
    load_pyth_data,
    process_loaded_data,
    downsize_processed_data,
)
from visualize import plot_confidence_over_time
from analysis import (
    calculate_returns,
    detect_breaches,
    extract_previous_returns,
    calculate_correlations,
)


def main():
    df = load_pyth_data(INPUT_CSV_PATH)
    df = process_loaded_data(df)
    df_sampled = downsize_processed_data(df, 10000, 100)
    plot_confidence_over_time(
        df_sampled, CONFIDENCE_THRESHOLD_BPS, f"{PLOT_OUTPUT_DIR}/confidence_over_time"
    )

    df_extended = calculate_returns(df)
    breaches_df = detect_breaches(df_extended, CONFIDENCE_THRESHOLD_BPS)
    breaches_info_df = extract_previous_returns(
        df_extended, breaches_df.index, RETURN_LOOKBACK_PERIODS
    )
    calculate_correlations(breaches_info_df, CORRELATION_METHOD)


if __name__ == "__main__":
    main()
