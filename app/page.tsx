'use client';

import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import ResultsDisplay from './components/ResultsDisplay';
import './styles/globals.css';

export default function Home() {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleUploadStart = () => {
    setLoading(true);
  };

  const handleUploadComplete = (data: any) => {
    setResults(data);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-primary-700 text-white shadow-md">
        <div className="container mx-auto py-6">
          <h1 className="text-3xl font-bold text-center">
            Quantum Medical Image Scanner
          </h1>
          <p className="text-center mt-2 text-primary-100">
            Leveraging quantum computing for advanced medical image analysis
          </p>
        </div>
      </header>

      <main className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto">
          {!results && !loading && (
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-2xl font-semibold mb-6 text-center text-primary-700">
                Upload a Medical Scan
              </h2>
              <p className="text-gray-600 mb-6 text-center">
                Upload your medical scan image to analyze it using our quantum computing algorithms.
                We support various types of medical images including X-rays, MRIs, CT scans, and ultrasound images.
              </p>
              <UploadForm 
                onUploadComplete={handleUploadComplete}
                onUploadStart={handleUploadStart}
              />
            </div>
          )}

          {loading && (
            <div className="text-center py-12">
              <div className="loading-spinner mx-auto"></div>
              <p className="mt-4 text-gray-600">
                Processing your scan with quantum algorithms...
              </p>
              <p className="text-sm text-gray-500 mt-2">
                This may take a moment as the quantum calculations are performed.
              </p>
            </div>
          )}

          {results && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold text-primary-700">
                  Analysis Results
                </h2>
                <button
                  onClick={() => setResults(null)}
                  className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded transition-colors"
                >
                  Upload New Scan
                </button>
              </div>
              <ResultsDisplay results={results} />
            </div>
          )}
        </div>
      </main>

      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4">
          <p className="text-center text-gray-400">
            Quantum Medical Image Scanner &copy; {new Date().getFullYear()} - 
            Leveraging quantum libraries like Qiskit and PennyLane for advanced medical image analysis
          </p>
        </div>
      </footer>
    </div>
  );
} 