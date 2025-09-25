import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const CryptoQuantLab = () => {
  const [availableCryptos, setAvailableCryptos] = useState([]);
  const [selectedCryptos, setSelectedCryptos] = useState([
    "BTC-USD",
    "ETH-USD",
    "ADA-USD",
  ]);
  const [timeframe, setTimeframe] = useState("1y");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [analysisLogs, setAnalysisLogs] = useState([]);
  const [apiStatus, setApiStatus] = useState("checking");
  const [historicalData, setHistoricalData] = useState(null);

  const API_BASE_URL = "http://localhost:8000/api";

  const timeframes = [
    { value: "3mo", label: "3 Months" },
    { value: "6mo", label: "6 Months" },
    { value: "1y", label: "1 Year" },
    { value: "2y", label: "2 Years" },
    { value: "5y", label: "5 Years" },
  ];

  useEffect(() => {
    checkApiHealth();
    fetchAvailableCryptos();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (response.ok) {
        setApiStatus("connected");
      } else {
        setApiStatus("error");
      }
    } catch (error) {
      setApiStatus("disconnected");
      console.error("API health check failed:", error);
    }
  };

  const fetchAvailableCryptos = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/available-cryptos`);
      if (response.ok) {
        const data = await response.json();
        setAvailableCryptos(data.cryptos);
      }
    } catch (error) {
      console.error("Failed to fetch available cryptos:", error);
      setAvailableCryptos([
        "BTC-USD",
        "ETH-USD",
        "ADA-USD",
        "SOL-USD",
        "LINK-USD",
      ]);
    }
  };

  const handleCryptoChange = (crypto) => {
    setSelectedCryptos((prev) =>
      prev.includes(crypto)
        ? prev.filter((c) => c !== crypto)
        : [...prev, crypto],
    );
  };

  const runAnalysis = async () => {
    if (selectedCryptos.length < 2) {
      alert("Pick at least 2 cryptocurrencies to analyze");
      return;
    }

    if (apiStatus !== "connected") {
      alert("API server not running. Start it with: python api_server.py");
      return;
    }

    setIsAnalyzing(true);
    setAnalysisLogs(["Starting analysis..."]);
    setResults(null);
    setHistoricalData(null);

    try {
      const historicalResponse = await fetch(
        `${API_BASE_URL}/historical-data`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            cryptos: selectedCryptos,
            timeframe: timeframe,
          }),
        },
      );

      if (historicalResponse.ok) {
        const historicalResult = await historicalResponse.json();
        setHistoricalData(historicalResult.data);
      }

      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          cryptos: selectedCryptos,
          timeframe: timeframe,
        }),
      });

      if (response.ok) {
        const result = await response.json();

        if (result.status === "success") {
          setResults(result);
        } else {
          setAnalysisLogs((prev) => [
            ...prev,
            `Analysis failed: ${result.error}`,
          ]);
        }
      } else {
        const errorResult = await response.json();
        setAnalysisLogs((prev) => [
          ...prev,
          `API Error: ${errorResult.error || "Unknown error"}`,
        ]);
      }
    } catch (error) {
      console.error("Analysis failed:", error);
      setAnalysisLogs((prev) => [...prev, `Network error: ${error.message}`]);
    }

    setIsAnalyzing(false);
  };

  const runQuickAnalysis = async () => {
    if (selectedCryptos.length < 2) {
      alert("Pick at least 2 cryptocurrencies to analyze");
      return;
    }

    try {
      setAnalysisLogs(["Running quick analysis..."]);

      const response = await fetch(`${API_BASE_URL}/quick-analysis`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          cryptos: selectedCryptos,
          timeframe: timeframe,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        setAnalysisLogs((prev) => [...prev, "Quick analysis done!"]);
        console.log("Quick analysis results:", result);
      }
    } catch (error) {
      setAnalysisLogs((prev) => [
        ...prev,
        `Quick analysis failed: ${error.message}`,
      ]);
    }
  };

  const formatPercentage = (value) => `${(value * 100).toFixed(2)}%`;
  const formatNumber = (value, decimals = 3) =>
    value?.toFixed(decimals) || "0.000";

  const COLORS = [
    "#0088FE",
    "#00C49F",
    "#FFBB28",
    "#FF8042",
    "#8884D8",
    "#82CA9D",
  ];

  const createPortfolioData = () => {
    if (!results?.portfolio?.optimal_weights) return [];

    return Object.entries(results.portfolio.optimal_weights).map(
      ([crypto, weight], index) => ({
        name: crypto.replace("-USD", ""),
        value: weight,
        color: COLORS[index % COLORS.length],
      }),
    );
  };

  const createPerformanceData = () => {
    if (!results?.strategies) return [];

    return [
      { name: "Momentum", sharpe: results.strategies.momentum_sharpe || 0 },
      {
        name: "Mean Reversion",
        sharpe: results.strategies.mean_reversion_sharpe || 0,
      },
      { name: "Combined", sharpe: results.strategies.combined_sharpe || 0 },
      {
        name: "Optimal Portfolio",
        sharpe: results.portfolio?.optimal_sharpe || 0,
      },
    ];
  };

  const getApiStatusColor = () => {
    switch (apiStatus) {
      case "connected":
        return "text-green-600";
      case "disconnected":
        return "text-red-600";
      case "error":
        return "text-yellow-600";
      default:
        return "text-gray-600";
    }
  };

  const getApiStatusText = () => {
    switch (apiStatus) {
      case "connected":
        return "Connected";
      case "disconnected":
        return "Not Connected";
      case "error":
        return "Connection Error";
      default:
        return "Checking...";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                Crypto QuantLab
              </h1>
              <p className="text-gray-600">
                Advanced quantitative analysis platform with Bayesian VECM,
                systematic strategies, and portfolio optimization
              </p>
            </div>
            <div className={`text-sm font-medium ${getApiStatusColor()}`}>
              {getApiStatusText()}
            </div>
          </div>
        </div>

        {apiStatus !== "connected" && (
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-yellow-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-yellow-700">
                  <strong>Server not running:</strong> Start the API server with{" "}
                  <code>python api_server.py</code>
                </p>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                Select Cryptocurrencies ({selectedCryptos.length}/
                {availableCryptos.length})
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-48 overflow-y-auto">
                {availableCryptos.map((crypto) => (
                  <label
                    key={crypto}
                    className="flex items-center space-x-2 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={selectedCryptos.includes(crypto)}
                      onChange={() => handleCryptoChange(crypto)}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm font-medium text-gray-700">
                      {crypto.replace("-USD", "")}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3">
                Time Period
              </h3>
              <select
                value={timeframe}
                onChange={(e) => setTimeframe(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                {timeframes.map((tf) => (
                  <option key={tf.value} value={tf.value}>
                    {tf.label}
                  </option>
                ))}
              </select>

              <div className="flex gap-2 mt-4">
                <button
                  onClick={runAnalysis}
                  disabled={
                    isAnalyzing ||
                    selectedCryptos.length < 2 ||
                    apiStatus !== "connected"
                  }
                  className={`flex-1 py-3 px-6 rounded-md font-semibold ${
                    isAnalyzing ||
                    selectedCryptos.length < 2 ||
                    apiStatus !== "connected"
                      ? "bg-gray-300 cursor-not-allowed text-gray-500"
                      : "bg-blue-600 hover:bg-blue-700 text-white"
                  }`}
                >
                  {isAnalyzing ? "Analyzing..." : "Run Full Analysis"}
                </button>

                <button
                  onClick={runQuickAnalysis}
                  disabled={
                    isAnalyzing ||
                    selectedCryptos.length < 2 ||
                    apiStatus !== "connected"
                  }
                  className={`py-3 px-4 rounded-md font-semibold ${
                    isAnalyzing ||
                    selectedCryptos.length < 2 ||
                    apiStatus !== "connected"
                      ? "bg-gray-300 cursor-not-allowed text-gray-500"
                      : "bg-green-600 hover:bg-green-700 text-white"
                  }`}
                >
                  Quick Test
                </button>
              </div>
            </div>
          </div>
        </div>

        {analysisLogs.length > 0 && (
          <div className="bg-gray-900 rounded-lg shadow-md p-6 mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">
              Analysis Progress
            </h3>
            <div className="space-y-2 font-mono text-sm max-h-64 overflow-y-auto">
              {analysisLogs.map((log, index) => (
                <div key={index} className="text-green-400">
                  {log}
                </div>
              ))}
              {isAnalyzing && (
                <div className="text-yellow-400 animate-pulse">
                  Processing...
                </div>
              )}
            </div>
          </div>
        )}

        {historicalData && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Historical Price Data
            </h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={historicalData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip
                  labelFormatter={(value) =>
                    new Date(value).toLocaleDateString()
                  }
                />
                <Legend />
                {selectedCryptos.map((crypto, index) => (
                  <Line
                    key={crypto}
                    type="monotone"
                    dataKey={crypto.replace("-USD", "")}
                    stroke={COLORS[index % COLORS.length]}
                    strokeWidth={2}
                    dot={false}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {results && results.status === "success" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="text-sm font-medium text-gray-500">
                  Cointegration Probability
                </div>
                <div className="text-2xl font-bold text-blue-600">
                  {formatPercentage(
                    results.bayesian_vecm.cointegration_probability,
                  )}
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  {results.bayesian_vecm.mcmc_simulations.toLocaleString()} MCMC
                  simulations
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="text-sm font-medium text-gray-500">
                  Best Strategy Sharpe
                </div>
                <div className="text-2xl font-bold text-green-600">
                  {formatNumber(results.strategies.combined_sharpe)}
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  Combined momentum + mean reversion
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="text-sm font-medium text-gray-500">
                  Portfolio Sharpe
                </div>
                <div className="text-2xl font-bold text-purple-600">
                  {formatNumber(results.portfolio.optimal_sharpe)}
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  Modern Portfolio Theory
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="text-sm font-medium text-gray-500">
                  Backtest Return
                </div>
                <div className="text-2xl font-bold text-orange-600">
                  {formatPercentage(results.backtest.total_return)}
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  Max drawdown:{" "}
                  {formatPercentage(results.backtest.max_drawdown)}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Strategy Performance (Sharpe Ratios)
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={createPerformanceData()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip
                      formatter={(value) => [
                        formatNumber(value),
                        "Sharpe Ratio",
                      ]}
                    />
                    <Bar dataKey="sharpe" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Optimal Portfolio Allocation
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={createPortfolioData()}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) =>
                        `${name}: ${formatPercentage(value)}`
                      }
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {createPortfolioData().map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => formatPercentage(value)} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {results && results.status === "error" && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-red-800 mb-2">
              Analysis Error
            </h3>
            <p className="text-red-700">{results.error}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CryptoQuantLab;
