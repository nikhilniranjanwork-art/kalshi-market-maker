# Kalshi Market Maker Bot

This project implements a market making strategy for Kalshi event contracts, focused on S&P 500 daily close brackets.

## Structure
- `src/` → Python source code (models, strategy, bot engine).
- `data/` → Historical S&P/market data for backtesting.
- `notebooks/` → Jupyter notebooks for experiments and analysis.

## First Goal
- Implement a probability model (Normal, Student-t, Cauchy) for bracket probabilities.
- Backtest on historical data and compare Brier scores.
- Later: integrate with Kalshi API and automate order placement.
