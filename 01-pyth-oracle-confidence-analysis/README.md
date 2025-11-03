# Exercise 01: Pyth price oracle confidence analysis

## Objective

Analyze Pyth Network oracle price feed data to identify periods of elevated price uncertainty and investigate their relationship with historical price dynamics.

## Background

Pyth price feeds include a confidence value (conf) representing the degree of uncertainty around each price point. This confidence value, combined with the price and exponent, forms a price estimate: price ± conf (both scaled by 10^expo).

## Scope

1. **Confidence Analysis**: Visualize confidence values over time to identify temporal patterns and anomalies in oracle price certainty.
2. **Breach Detection**: Identify instances where the confidence value exceeds 300 basis points (3% of the price), indicating periods of significant price uncertainty or oracle data quality issues.
3. **Price Return Correlation**: Calculate historical price returns preceding each confidence breach and analyze correlation patterns to determine if specific price movements predict elevated confidence values.

## Deliverables

1. Time series visualization of confidence values with breach thresholds.
2. Statistical summary of breach events (frequency, duration, magnitude).
3. Correlation analysis between antecedent price returns and confidence breaches.
4. Findings report identifying patterns and potential predictive indicators.

## Application

This analysis framework provides a generalized tool for assessing oracle reliability across any token pair, enabling risk assessment for DeFi protocols relying on Pyth Network price feeds.