"""
Main script to run Pyth oracle confidence analysis
"""

from config import INPUT_CSV_PATH, PLOT_OUTPUT_DIR, CONFIDENCE_THRESHOLD_BPS
from load_and_process_data import (
    load_pyth_data,
    process_loaded_data,
    downsize_processed_data,
)
from visualize import plot_confidence_over_time


def main():
    df_loaded = load_pyth_data(INPUT_CSV_PATH)
    df_processed = process_loaded_data(df_loaded)
    df_sampled = downsize_processed_data(df_processed, 1000000, 100)
    plot_confidence_over_time(df_sampled, CONFIDENCE_THRESHOLD_BPS, f"{PLOT_OUTPUT_DIR}/confidence_over_time")


if __name__ == "__main__":
    main()
