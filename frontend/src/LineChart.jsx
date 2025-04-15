import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
} from 'chart.js';

// Register chart elements with Chart.js
ChartJS.register(LinearScale, PointElement, LineElement, Tooltip);

const LineChart = ({ data }) => {
  const chartData = {
    labels: data.map((_, index) => index),
    datasets: [
      {
        label: 'Elo',
        data: data,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true, // Whether to fill the area under the line
        tension: 0.4, // Curve smoothness
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          type: 'linear',
          text: 'Runde',
        },
      },
      y: {
        title: {
          display: true,
          type: 'linear',
          text: 'Elo-Zahl',
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default LineChart;
