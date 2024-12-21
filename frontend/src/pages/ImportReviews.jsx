import { useState } from "react";
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from "recharts";
import { importCsvReviews, importJsonReviews } from "../api";
import '../styles/ImportReviews.css';

const SENTIMENT_COLORS = {
  very_positive: "#10B981",
  positive: "#34D399",
  neutral: "#6B7280",
  negative: "#EF4444",
  very_negative: "#DC2626"
};

export default function ImportReviews() {
  const [file, setFile] = useState(null);
  const [sentimentCounts, setSentimentCounts] = useState({});
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const token = localStorage.getItem("token");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    if (error) setError(null);
  };

  const handleUpload = async (importFunction) => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }
    setIsLoading(true);
    setError(null);

    try {
      const response = await importFunction(file, token);
      setSentimentCounts(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to import reviews. Please try again.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const chartData = Object.entries(sentimentCounts).map(([name, value]) => ({
    name,
    value
  }));

  return (
    <div className="dashboard-container">
      <div className="content-wrapper">
        <h2 className="dashboard-title">Sentiment Analysis Dashboard</h2>

        <section className="upload-section">
          {error && (
            <div className="error-alert">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              {error}
            </div>
          )}

          <div className="file-upload-container">
            <input
              type="file"
              accept=".csv,.json"
              onChange={handleFileChange}
              className="file-input"
              id="file-upload"
            />
          </div>

          <div className="button-group">
            <button
              onClick={() => handleUpload(importCsvReviews)}
              disabled={isLoading}
              className={`upload-button csv ${isLoading ? 'loading' : ''}`}
            >
              {isLoading ? "Uploading CSV..." : "Upload CSV"}
            </button>
            <button
              onClick={() => handleUpload(importJsonReviews)}
              disabled={isLoading}
              className={`upload-button json ${isLoading ? 'loading' : ''}`}
            >
              {isLoading ? "Uploading JSON..." : "Upload JSON"}
            </button>
          </div>
        </section>

        {Object.keys(sentimentCounts).length > 0 && (
          <section className="results-section">
            <h3 className="results-title">Analysis Results</h3>

            <div className="chart-container">
              <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                  <PieChart>
                    <Pie
                      data={chartData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius="90%"
                      label={({name, value}) => `${value}`}
                    >
                      {chartData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={SENTIMENT_COLORS[entry.name]}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        background: '#1a1a1a',
                        border: '1px solid #2d2d2d',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                    />
                    <Legend
                      formatter={(value) => value.replace(/_/g, ' ')}
                      wrapperStyle={{ color: '#e1e1e1' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="stats-grid">
              {Object.entries(sentimentCounts).map(([sentiment, count]) => (
                <div
                  key={sentiment}
                  className="stat-card"
                  style={{
                    borderLeft: `4px solid ${SENTIMENT_COLORS[sentiment]}`
                  }}
                >
                  <span className="stat-label">{sentiment.replace(/_/g, ' ')}</span>
                  <span className="stat-value">{count}</span>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}