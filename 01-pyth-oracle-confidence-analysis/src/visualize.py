"""
Visualization module for plotting confidence and analysis results
"""

import matplotlib.pyplot as plt
import matplotlib.dates as dt
from config import (
    FIGURE_SIZE,
    TIMESTAMP_COL,
    CONF_COL,
    FIGURE_DPI,
    PRIMARY_COLOR,
    ACCENT_COLOR,
    LINE_WIDTH_REGULAR,
    LINE_WIDTH_BOLD,
    FONT_SIZE_REGULAR,
    FONT_SIZE_MEDIUM,
    FONT_WEIGHT_BOLD,
    MIN_SPACE_X_TICKS,
)


def plot_confidence_over_time(df, threshold_bps=None, save_path=None):
    """
    Plot confidence values over time

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with timestamp and confidence columns
    threshold_bps : float, optional
        Confidence threshold in basis points to plot as horizontal line
    save_path : str, optional
        Path to save the plot. If None, plot is displayed but not saved
    """

    plt.figure(figsize=FIGURE_SIZE)

    # Plot confidence
    plt.plot(
        df[TIMESTAMP_COL],
        df[CONF_COL],
        linewidth=LINE_WIDTH_REGULAR,
        color=PRIMARY_COLOR,
        label="Confidence",
    )

    # Add threshold line if specified
    if threshold_bps is not None:
        threshold_value = threshold_bps
        plt.axhline(
            y=threshold_value,
            color=ACCENT_COLOR,
            linestyle="--",
            linewidth=LINE_WIDTH_BOLD,
            label="Threshold",
        )

    plt.xlabel("Time", fontsize=FONT_SIZE_REGULAR)
    plt.ylabel("Confidence", fontsize=FONT_SIZE_REGULAR)
    plt.title(
        "Pyth Oracle Confidence Over Time",
        fontsize=FONT_SIZE_MEDIUM,
        fontweight=FONT_WEIGHT_BOLD,
    )
    plt.legend(loc="upper right")
    ax = plt.gca()
    max_ticks = FIGURE_SIZE[0] // MIN_SPACE_X_TICKS
    ax.xaxis.set_major_locator(dt.AutoDateLocator(maxticks=max_ticks))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    plt.tight_layout()

    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()

    plt.close()
