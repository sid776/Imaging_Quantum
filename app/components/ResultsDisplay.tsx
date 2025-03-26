'use client';

import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface Anomaly {
  location: [number, number];
  intensity: number;
  type: string;
}

interface Metrics {
  entropy: number;
  contrast: number;
  brightness: number;
}

export interface ResultsDisplayProps {
  results: {
    metrics: Metrics;
    anomalies: Anomaly[];
    processed_image: string;
  };
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  if (!results) return null;

  const { metrics, anomalies, processed_image } = results;

  // Prepare data for charts
  const metricsBarData = {
    labels: ['Entropy', 'Contrast', 'Brightness'],
    datasets: [
      {
        label: 'Scan Metrics',
        data: [metrics.entropy, metrics.contrast, metrics.brightness],
        backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(75, 192, 192, 0.6)'],
        borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)'],
        borderWidth: 1,
      },
    ],
  };

  // Anomaly type distribution chart
  const anomalyTypeCount = anomalies.reduce((acc: Record<string, number>, anomaly) => {
    acc[anomaly.type] = (acc[anomaly.type] || 0) + 1;
    return acc;
  }, {});

  const anomalyDoughnutData = {
    labels: Object.keys(anomalyTypeCount),
    datasets: [
      {
        label: 'Anomaly Types',
        data: Object.values(anomalyTypeCount),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mt-8">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Analysis Results</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 className="text-lg font-semibold mb-3 text-gray-700">Processed Scan</h3>
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <img 
              src={processed_image} 
              alt="Processed Scan" 
              className="w-full h-auto object-contain"
            />
          </div>
        </div>
        
        <div>
          <h3 className="text-lg font-semibold mb-3 text-gray-700">Metrics</h3>
          <div className="h-64">
            <Bar 
              data={metricsBarData} 
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false,
                  },
                  tooltip: {
                    callbacks: {
                      label: function(context) {
                        return `${context.dataset.label}: ${context.raw.toFixed(4)}`;
                      }
                    }
                  }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                  },
                },
              }}
            />
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 className="text-lg font-semibold mb-3 text-gray-700">Anomaly Distribution</h3>
          <div className="h-64">
            <Doughnut 
              data={anomalyDoughnutData} 
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  tooltip: {
                    callbacks: {
                      label: function(context) {
                        const label = context.label || '';
                        const value = context.raw as number;
                        const total = (context.dataset.data as number[]).reduce((a, b) => (a as number) + (b as number), 0) as number;
                        const percentage = Math.round((value / total) * 100);
                        return `${label}: ${value} (${percentage}%)`;
                      }
                    }
                  }
                }
              }}
            />
          </div>
        </div>
        
        <div>
          <h3 className="text-lg font-semibold mb-3 text-gray-700">Detected Anomalies</h3>
          <div className="overflow-auto max-h-64 border border-gray-200 rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Intensity</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {anomalies.map((anomaly, index) => (
                  <tr key={index}>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-600">
                      [{anomaly.location[0]}, {anomaly.location[1]}]
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-600">
                      {anomaly.type}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-600">
                      {anomaly.intensity.toFixed(3)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-3 text-gray-700">Summary</h3>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600 mb-2">
            <span className="font-medium">Total Anomalies:</span> {anomalies.length}
          </p>
          <p className="text-sm text-gray-600 mb-2">
            <span className="font-medium">Average Intensity:</span> {anomalies.length > 0 
              ? (anomalies.reduce((sum, a) => sum + a.intensity, 0) / anomalies.length).toFixed(3) 
              : 'N/A'
            }
          </p>
          <p className="text-sm text-gray-600">
            <span className="font-medium">Image Entropy:</span> {metrics.entropy.toFixed(3)}
          </p>
        </div>
      </div>
    </div>
  );
} 