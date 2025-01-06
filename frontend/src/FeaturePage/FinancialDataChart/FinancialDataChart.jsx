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
    labels: data.labels, // e.g., ['Jan', 'Feb', 'Mar', ...]
    datasets: [
      {
        label: 'Financial Metric',
        data: data.values, // e.g., [100, 200, 150, ...]
        fill: false,
        backgroundColor: '#6366F1', // Indigo-500
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

export default FinancialDataChart;
