"""
Configuration file for Pyth Oracle Confidence Analysis
Modify parameters here to customize the analysis
"""

# ============================================================================
# DATA CONFIGURATION
# ============================================================================

# Path to input CSV file
INPUT_CSV_PATH = "data/raw/prices.csv"


# ============================================================================
# ANALYSIS PARAMETERS
# ============================================================================

# Confidence breach threshold in basis points (300 bps = 3%)
CONFIDENCE_THRESHOLD_BPS = 300
# Lookback period for calculating price returns before breach (in data points)
RETURN_LOOKBACK_PERIODS = 10
# Correlation method: "pearson", "kendall", or "spearman"
CORRELATION_METHOD = "pearson"


# ============================================================================
# VISUALIZATION PARAMETERS
# ============================================================================

# Output directory for plots
PLOT_OUTPUT_DIR = "outputs/plots/"
# Output directory for reports
REPORT_OUTPUT_DIR = "outputs/reports/"
# Figure size for plots (width, height in inches)
FIGURE_SIZE = (14, 8)
# DPI for saved figures
FIGURE_DPI = 300
LINE_WIDTH_REGULAR = 1
LINE_WIDTH_BOLD = 2
MIN_SPACE_X_TICKS = 0.5
FONT_SIZE_REGULAR = 12
FONT_SIZE_MEDIUM = 14
FONT_WEIGHT_BOLD = "bold"
PRIMARY_COLOR = "#5e4c5f"
SECONDARY_COLOR = "#999999"
ACCENT_COLOR = "#ffbb6f"

# ============================================================================
# DATA PROCESSING
# ============================================================================

# Column names in Pyth CSV
TIMESTAMP_COL = "publishTime"
PRICE_COL = "price"
CONF_COL = "confidence"

# Timezone for timestamp conversion
TIMEZONE = "UTC"
