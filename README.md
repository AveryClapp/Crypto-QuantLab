# Crypto QuantLab

Quick quantitative analysis for crypto markets.

## What It Does

- **Cointegration testing** (Johansen) with 10,000 Monte Carlo bootstrap simulations
- **Systematic strategies** - momentum + mean reversion
- **Portfolio optimization** - mean-variance framework
- **Statistical arbitrage** - pairs trading on cointegrated assets
- **Comprehensive backtesting**

**Result:** Full quant analysis in 30 seconds.

## Quick Math

### Cointegration

```
Johansen test → trace statistic vs critical value
Bootstrap: resample 10,000x, test each → probability
```

### Strategies

```
Momentum: rank(Σ returns[-21:]) → long winners, short losers
Mean Reversion: z-score → fade extremes (|z| > 2)
Combined: (momentum + mean_reversion) / 2
```

### Portfolio

```
maximize: (μᵀw) / √(wᵀΣw)
subject to: Σwᵢ = 1, wᵢ ≥ 0
```

### Arbitrage

```
spread = price₁ - β×price₂
z = (spread - μ) / σ
trade when |z| > 2
```

## Run It

```bash
pip install numpy pandas scipy scikit-learn yfinance statsmodels

python crypto_quantlab.py
```

Done in ~30 seconds.

## Extend It

### More assets

```python
lab.cryptos = ['BTC-USD', 'ETH-USD', 'MATIC-USD', 'AVAX-USD']
```

### Longer period

```python
lab.fetch_data(period='2y')
```

### New strategies

```python
def pairs_trading(self):
    # Your strategy here
    pass
```

## What's Next

- [ ] Web playground for portfolio construction
- [ ] Exchange API integration
- [ ] GARCH volatility models
- [ ] Regime-switching (Markov)

---

**Built with:** NumPy, pandas, SciPy, statsmodels, yfinance
