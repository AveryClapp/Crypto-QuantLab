// src/components/FinancialDataChart.js
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const FinancialDataChart = ({ data }) => {
  // Assuming 'data' has 'labels' and 'values'
  const chartData = {
    labels:	data.labels, // e.g., ['Jan', 'Feb', 'Mar', ...]
    datasets: [
      {
        label: 'Financial Metric',
        data: data.values, 
        fill: false,
        backgroundColor: '#6366F1', 
        borderColor: '#6366F1',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Recent Financial Data',
      },
    },
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <Line data={chartData} options={options} />
    </div>
  );
};


const MetricsTable = ({ metrics }) => {
		console.log(metrics);
		return (
				<div>
				<Typography variant="h5" component="h2" gutterBottom>
				Market Metrics
				</Typography>
				<TableContainer component={Paper}>
				<Table>
				<TableHead>
				<TableRow>
				<TableCell>Metric</TableCell>
				<TableCell align="right">Value</TableCell>
				</TableRow>
				</TableHead>
				<TableBody>
				{metrics && (
						<>
						<TableRow>
						<TableCell>Price</TableCell>
						<TableCell align="right">${metrics.price}</TableCell>
						</TableRow>
						<TableRow>
						<TableCell>Daily Volume</TableCell>
						<TableCell align="right">${metrics.daily_volume}</TableCell>
						</TableRow>
						<TableRow>
						<TableCell>Daily Volume Change</TableCell>
						<TableCell align="right">{metrics.daily_volume_change}%</TableCell>
						</TableRow>
						<TableRow>
						<TableCell>Market Cap</TableCell>
						<TableCell align="right">${metrics.market_cap}</TableCell>
						</TableRow>
						<TableRow>
						<TableCell>Daily Delta</TableCell>
						<TableCell align="right">{metrics.daily_delta}%</TableCell>
						</TableRow>
						<TableRow>
						<TableCell>Weekly Delta</TableCell>
						<TableCell align="right">{metrics.weekly_delta}%</TableCell>
						</TableRow>
						<TableRow>
						<TableCell>Fear and Greed Index</TableCell>
						<TableCell align="right">{metrics.fear_and_greed}</TableCell>
						</TableRow>
						<TableRow>
						<TableCell>BTC Dominance</TableCell>
						<TableCell align="right">{metrics.btc_dominance}%</TableCell>
						</TableRow>
						<TableRow>
						<TableCell>Stablecoin Volume</TableCell>
						<TableCell align="right">${metrics.stablecoin_volume}</TableCell>
						</TableRow>
						<TableRow>
						<TableCell>Total Market Cap</TableCell>
						<TableCell align="right">${metrics.total_market_cap}</TableCell>
						</TableRow>
						</>
				)}
				</TableBody>
				</Table>
				</TableContainer>
				</div>
		);
};

export default MetricsTable;
