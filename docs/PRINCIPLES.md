# Principles

Non-negotiable operating rules for this repository. When a proposed change
conflicts with one of these, the principle wins.

- No live trades without explicit human approval.
- No strategy without a reproducible backtest.
- No backtest without fees, slippage, and conservative fill assumptions.
  Market orders cross the spread and include fees/slippage. Limit-order
  fill-at-touch is optimistic and may only be used when explicitly labeled
  and justified.
- No AI signal is ever the sole basis for a trading decision.
- Every external data source goes through an `Exchange` adapter — no
  direct API calls from research, backtesting, or strategy code.
- Every experiment must be reproducible: fixed data version, fixed code
  version, fixed parameters, logged results.
- Raw data is preserved. Cleaning and interpretation happen visibly, in
  code that can be reviewed and re-run — never silently.
- Results are always labeled by stage: hypothesis, backtest, out-of-sample,
  paper trade, or live trade. A backtest result never implies future
  returns.
