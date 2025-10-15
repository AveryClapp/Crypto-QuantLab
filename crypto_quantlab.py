import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats
from scipy.optimize import minimize
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class CryptoQuantLab:
    def __init__(self):
        self.cryptos = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'SOL-USD', 'LINK-USD']
        self.data = None
        self.results = {}

    def fetch_data(self, period='1y'):
        data = yf.download(self.cryptos, period=period)["Close"]
        self.data = data.dropna()
        return self.data

    def cointegration_analysis(self):
        """Johansen cointegration testing with bootstrap robustness"""
        log_prices = np.log(self.data.iloc[:, :3])

        # Johansen cointegration test
        johansen_result = coint_johansen(log_prices, det_order=0, k_ar_diff=1)
        trace_stat = johansen_result.lr1[0]
        critical_value_95 = johansen_result.cvt[0, 1]
        is_cointegrated = trace_stat > critical_value_95

        n_simulations = 10000
        cointegration_scores = []

        for i in range(n_simulations):
            sample_idx = np.random.choice(len(log_prices), size=len(log_prices), replace=True)
            sample_data = log_prices.iloc[sample_idx]

            try:
                boot_result = coint_johansen(sample_data, det_order=0, k_ar_diff=1)
                boot_trace = boot_result.lr1[0]
                boot_critical = boot_result.cvt[0, 1]
                cointegration_scores.append(1 if boot_trace > boot_critical else 0)
            except:
                cointegration_scores.append(0)

        cointegration_prob = np.mean(cointegration_scores)

        arbitrage_pairs = []
        for i in range(len(log_prices.columns)):
            for j in range(i+1, len(log_prices.columns)):
                score, pvalue, _ = coint(log_prices.iloc[:, i], log_prices.iloc[:, j])
                if pvalue < 0.05:
                    pair = (log_prices.columns[i], log_prices.columns[j])
                    arbitrage_pairs.append(pair)

        self.results['cointegration'] = {
            'is_cointegrated': is_cointegrated,
            'johansen_trace_statistic': float(trace_stat),
            'johansen_critical_value_95': float(critical_value_95),
            'cointegration_probability': float(cointegration_prob),
            'mcmc_simulations': n_simulations,
            'arbitrage_opportunities': arbitrage_pairs
        }

        print(f"Cointegration test: {trace_stat:.2f} vs {critical_value_95:.2f} critical → {'✓ cointegrated' if is_cointegrated else '✗ not cointegrated'}")
        print(f"Bootstrap probability from {n_simulations:,} simulations: {cointegration_prob:.3f}")
        print(f"Found {len(arbitrage_pairs)} cointegrated pairs")

        return self.results['cointegration']

    def systematic_strategies(self):
        returns = self.data.pct_change().dropna()

        momentum_lookback = 21
        momentum_scores = returns.rolling(momentum_lookback).sum()
        momentum_signals = momentum_scores.rank(axis=1, pct=True)
        momentum_positions = np.where(momentum_signals > 0.6, 1,
                                      np.where(momentum_signals < 0.4, -1, 0))
        momentum_positions = pd.DataFrame(momentum_positions, index=returns.index, columns=returns.columns)
        momentum_returns = (momentum_positions.shift(1) * returns).sum(axis=1)
        momentum_sharpe = momentum_returns.mean() / momentum_returns.std() * np.sqrt(252)

        z_scores = (self.data - self.data.rolling(20).mean()) / self.data.rolling(20).std()
        mean_rev_positions = np.where(z_scores < -2, 1, np.where(z_scores > 2, -1, 0))
        mean_rev_positions = pd.DataFrame(mean_rev_positions, index=self.data.index, columns=self.data.columns)
        mean_rev_returns = (mean_rev_positions.shift(1) * returns).sum(axis=1)
        mean_rev_sharpe = mean_rev_returns.mean() / mean_rev_returns.std() * np.sqrt(252)

        combined_returns = (momentum_returns + mean_rev_returns) / 2
        combined_sharpe = combined_returns.mean() / combined_returns.std() * np.sqrt(252)

        self.results['strategies'] = {
            'momentum_sharpe': momentum_sharpe,
            'mean_reversion_sharpe': mean_rev_sharpe,
            'combined_sharpe': combined_sharpe,
            'momentum_returns': momentum_returns,
            'mean_reversion_returns': mean_rev_returns,
            'combined_returns': combined_returns
        }

        print(f"Momentum Sharpe: {momentum_sharpe:.3f} | Mean reversion: {mean_rev_sharpe:.3f} | Combined: {combined_sharpe:.3f}")

        return self.results['strategies']

    def portfolio_optimization(self):
        returns = self.data.pct_change().dropna()
        mean_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252

        n_assets = len(returns.columns)

        def portfolio_performance(weights):
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            return portfolio_return, portfolio_std

        def negative_sharpe(weights):
            p_return, p_std = portfolio_performance(weights)
            return -(p_return / p_std)

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(n_assets))

        result = minimize(negative_sharpe, 
                          x0=np.array([1/n_assets] * n_assets),
                          method='SLSQP',
                          bounds=bounds,
                          constraints=constraints)

        optimal_weights = result.x
        opt_return, opt_std = portfolio_performance(optimal_weights)
        opt_sharpe = opt_return / opt_std

        self.results['portfolio'] = {
            'optimal_weights': dict(zip(returns.columns, optimal_weights)),
            'expected_return': opt_return,
            'volatility': opt_std,
            'sharpe_ratio': opt_sharpe
        }

        print(f"Optimal Sharpe: {opt_sharpe:.3f} with {opt_return*100:.2f}% return and {opt_std*100:.2f}% volatility")

        return self.results['portfolio']

    def comprehensive_backtest(self):
        returns = self.data.pct_change().dropna()
        strategy_returns = self.results['strategies']['combined_returns']

        total_return = (1 + strategy_returns).prod() - 1
        annualized_return = (1 + strategy_returns).prod() ** (252 / len(strategy_returns)) - 1
        volatility = strategy_returns.std() * np.sqrt(252)
        sharpe_ratio = annualized_return / volatility

        cumulative = (1 + strategy_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()

        self.results['backtest'] = {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': len(strategy_returns),
            'win_rate': len(strategy_returns[strategy_returns > 0]) / len(strategy_returns)
        }

        print(f"Total return: {total_return*100:.2f}% | Sharpe: {sharpe_ratio:.3f} | Max drawdown: {max_drawdown*100:.2f}% | Win rate: {self.results['backtest']['win_rate']*100:.1f}%")

        return self.results['backtest']

    def quantify_cointegration_arbitrage(self):
        arbitrage_pairs = self.results['cointegration']['arbitrage_opportunities']

        opportunities = []
        for pair in arbitrage_pairs:
            asset1, asset2 = pair
            prices1 = self.data[asset1]
            prices2 = self.data[asset2]

            slope = np.cov(prices1, prices2)[0,1] / np.var(prices2)
            spread = prices1 - slope * prices2
            current_z = (spread.iloc[-1] - spread.mean()) / spread.std()

            if abs(current_z) > 2:
                direction = "LONG" if current_z < -2 else "SHORT"
                opportunities.append({
                    'pair': f"{asset1}-{asset2}",
                    'z_score': float(current_z),
                    'direction': direction,
                    'expected_profit': float(abs(current_z) * spread.std())
                })

        total_opportunity_value = sum([op['expected_profit'] for op in opportunities])

        self.results['arbitrage'] = {
            'opportunities': opportunities,
            'total_pairs_analyzed': len(arbitrage_pairs),
            'active_opportunities': len(opportunities),
            'total_opportunity_value': total_opportunity_value
        }

        print(f"Analyzed {len(arbitrage_pairs)} pairs → {len(opportunities)} active arbitrage opportunities worth ${total_opportunity_value:.2f}")

        return self.results['arbitrage']

    def generate_summary_report(self):
        print(f"\n{'='*50}")
        print(f"CRYPTO QUANTLAB SUMMARY")
        print(f"{'='*50}\n")

        print(f"Data: {len(self.data.columns)} assets, {len(self.data):,} observations")
        print(f"Period: {self.data.index[0].strftime('%Y-%m-%d')} to {self.data.index[-1].strftime('%Y-%m-%d')}\n")

        if 'cointegration' in self.results:
            print(f"Cointegration: {self.results['cointegration']['mcmc_simulations']:,} simulations → {self.results['cointegration']['cointegration_probability']:.3f} probability")
            print(f"Pairs found: {len(self.results['cointegration']['arbitrage_opportunities'])}\n")

        if 'strategies' in self.results:
            print(f"Best strategy Sharpe: {self.results['strategies']['combined_sharpe']:.3f}")
            print(f"  ↳ Momentum: {self.results['strategies']['momentum_sharpe']:.3f}")
            print(f"  ↳ Mean reversion: {self.results['strategies']['mean_reversion_sharpe']:.3f}\n")

        if 'portfolio' in self.results:
            print(f"Optimal portfolio Sharpe: {self.results['portfolio']['sharpe_ratio']:.3f}")
            print(f"Expected return: {self.results['portfolio']['expected_return']*100:.2f}% | Volatility: {self.results['portfolio']['volatility']*100:.2f}%\n")

        if 'backtest' in self.results:
            print(f"Backtest: {self.results['backtest']['total_return']*100:.2f}% return")
            print(f"Sharpe: {self.results['backtest']['sharpe_ratio']:.3f} | Max DD: {self.results['backtest']['max_drawdown']*100:.2f}%\n")

        if 'arbitrage' in self.results:
            print(f"Arbitrage: {self.results['arbitrage']['active_opportunities']} opportunities")
            print(f"Total value: ${self.results['arbitrage']['total_opportunity_value']:.2f}\n")

        print(f"{'='*50}\n")


def main():
    lab = CryptoQuantLab()

    print("Fetching crypto data...\n")
    lab.fetch_data()

    lab.cointegration_analysis()
    print()
    lab.systematic_strategies()
    print()
    lab.portfolio_optimization()
    print()
    lab.comprehensive_backtest()
    print()
    lab.quantify_cointegration_arbitrage()

    lab.generate_summary_report()

if __name__ == "__main__":
    main()
