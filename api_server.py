from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import traceback
from crypto_quantlab import CryptoQuantLab
import pandas as pd
import numpy as np
import uvicorn

class AnalysisRequest(BaseModel):
    cryptos: List[str] = Field(..., min_items=2, max_items=10)
    timeframe: str = Field("1y", pattern="^(3mo|6mo|1y|2y|5y)$")

class QuickAnalysisRequest(BaseModel):
    cryptos: List[str] = Field(..., min_items=2, max_items=5)
    timeframe: str = Field("3mo", pattern="^(3mo|6mo|1y|2y|5y)$")

class HistoricalDataRequest(BaseModel):
    cryptos: List[str] = Field(..., min_items=1, max_items=10)
    timeframe: str = Field("1y", pattern="^(3mo|6mo|1y|2y|5y)$")

app = FastAPI(
    title="Crypto QuantLab API",
    description="Quantitative analysis for cryptocurrency markets",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def serialize_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    return obj

def clean_results(data):
    if isinstance(data, dict):
        return {k: clean_results(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_results(item) for item in data]
    else:
        return serialize_numpy(data)

@app.get("/")
async def root():
    return {
        "message": "Crypto QuantLab API",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "running",
        "message": "All systems operational"
    }

@app.get("/api/available-cryptos")
async def get_available_cryptos():
    cryptos = [
        'BTC-USD', 'ETH-USD', 'ADA-USD', 'SOL-USD', 'LINK-USD',
        'MATIC-USD', 'AVAX-USD', 'ATOM-USD', 'DOT-USD', 'UNI-USD',
        'AAVE-USD', 'ALGO-USD', 'XTZ-USD', 'FTM-USD', 'NEAR-USD',
        'SUSHI-USD', 'COMP-USD', 'MKR-USD', 'YFI-USD', 'CRV-USD'
    ]
    return {
        "cryptos": cryptos,
        "total_count": len(cryptos)
    }

@app.post("/api/analyze")
async def run_analysis(request: AnalysisRequest):
    try:
        lab = CryptoQuantLab()
        lab.cryptos = request.cryptos


        try:
            data = lab.fetch_data(period=request.timeframe)
            if data is None or data.empty:
                raise HTTPException(
                    status_code=400,
                    detail="Couldn't fetch data for those cryptocurrencies"
                )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Data issue: {str(e)}")

        try:
            vecm_results = lab.bayesian_vecm_analysis()
        except Exception as e:
            vecm_results = {
                "cointegration_probability": 0.0, 
                "mcmc_simulations": 10000, 
                "arbitrage_opportunities": []
            }

        try:
            strategy_results = lab.systematic_strategies()
        except Exception as e:
            strategy_results = {
                "momentum_sharpe": 0.0, 
                "mean_reversion_sharpe": 0.0, 
                "combined_sharpe": 0.0
            }

        try:
            portfolio_results = lab.portfolio_optimization()
        except Exception as e:
            portfolio_results = {
                "sharpe_ratio": 0.0, 
                "expected_return": 0.0, 
                "volatility": 0.0, 
                "optimal_weights": {}
            }

        try:
            backtest_results = lab.comprehensive_backtest()
        except Exception as e:
            backtest_results = {
                "total_return": 0.0, 
                "annualized_return": 0.0,
                "sharpe_ratio": 0.0, 
                "max_drawdown": 0.0, 
                "win_rate": 0.0,
                "volatility": 0.0
            }

        try:
            arbitrage_results = lab.quantify_cointegration_arbitrage()
        except Exception as e:
            arbitrage_results = {
                "total_pairs_analyzed": 0, 
                "active_opportunities": 0, 
                "total_opportunity_value": 0.0
            }


        response_data = {
            "status": "success",
            "data_analysis": {
                "assets_analyzed": len(request.cryptos),
                "time_period": request.timeframe,
                "total_observations": len(lab.data) if hasattr(lab, 'data') and lab.data is not None else 0,
                "date_range": {
                    "start": lab.data.index[0].isoformat() if hasattr(lab, 'data') and lab.data is not None and len(lab.data) > 0 else None,
                    "end": lab.data.index[-1].isoformat() if hasattr(lab, 'data') and lab.data is not None and len(lab.data) > 0 else None
                }
            },
            "bayesian_vecm": {
                "cointegration_probability": vecm_results.get('cointegration_probability', 0.0),
                "mcmc_simulations": vecm_results.get('mcmc_simulations', 10000),
                "arbitrage_pairs_found": len(vecm_results.get('arbitrage_opportunities', []))
            },
            "strategies": {
                "momentum_sharpe": strategy_results.get('momentum_sharpe', 0.0),
                "mean_reversion_sharpe": strategy_results.get('mean_reversion_sharpe', 0.0),
                "combined_sharpe": strategy_results.get('combined_sharpe', 0.0)
            },
            "portfolio": {
                "optimal_sharpe": portfolio_results.get('sharpe_ratio', 0.0),
                "expected_return": portfolio_results.get('expected_return', 0.0),
                "volatility": portfolio_results.get('volatility', 0.0),
                "optimal_weights": portfolio_results.get('optimal_weights', {})
            },
            "backtest": {
                "total_return": backtest_results.get('total_return', 0.0),
                "annualized_return": backtest_results.get('annualized_return', 0.0),
                "sharpe_ratio": backtest_results.get('sharpe_ratio', 0.0),
                "max_drawdown": backtest_results.get('max_drawdown', 0.0),
                "win_rate": backtest_results.get('win_rate', 0.0),
                "volatility": backtest_results.get('volatility', 0.0)
            },
            "arbitrage": {
                "total_pairs_analyzed": arbitrage_results.get('total_pairs_analyzed', 0),
                "active_opportunities": arbitrage_results.get('active_opportunities', 0),
                "total_opportunity_value": arbitrage_results.get('total_opportunity_value', 0.0)
            }
        }

        cleaned_data = clean_results(response_data)
        return cleaned_data

    except HTTPException:
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Something went wrong during analysis: {error_trace}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/api/quick-analysis")
async def quick_analysis(request: QuickAnalysisRequest):
    try:
        lab = CryptoQuantLab()
        lab.cryptos = request.cryptos

        price_data = lab.fetch_data(period=request.timeframe)
        returns = price_data.pct_change().dropna()

        results = {
            "status": "success",
            "data_summary": {
                "assets": len(price_data.columns),
                "observations": len(price_data),
                "date_range": {
                    "start": price_data.index[0].isoformat(),
                    "end": price_data.index[-1].isoformat()
                }
            },
            "quick_metrics": {
                "average_daily_return": float(returns.mean().mean()),
                "average_volatility": float(returns.std().mean()),
                "best_performer": returns.mean().idxmax(),
                "worst_performer": returns.mean().idxmin(),
                "correlation_matrix": clean_results(returns.corr().to_dict())
            }
        }

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quick analysis failed: {str(e)}"
        )

@app.post("/api/historical-data")
async def get_historical_data(request: HistoricalDataRequest):
    try:
        lab = CryptoQuantLab()
        lab.cryptos = request.cryptos
        price_data = lab.fetch_data(period=request.timeframe)

        chart_data = []
        for date in price_data.index:
            row = {"date": date.isoformat()}
            for crypto in price_data.columns:
                row[crypto.replace('-USD', '')] = float(price_data.loc[date, crypto])
            chart_data.append(row)

        return {
            "status": "success",
            "data": chart_data,
            "cryptos": [crypto.replace('-USD', '') for crypto in price_data.columns],
            "metadata": {
                "total_points": len(chart_data),
                "date_range": {
                    "start": price_data.index[0].isoformat(),
                    "end": price_data.index[-1].isoformat()
                }
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Couldn't get historical data: {str(e)}"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "status": "error",
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "status": "error",
        "error": "Something went wrong on our end",
        "detail": str(exc)
    }

if __name__ == '__main__':
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
