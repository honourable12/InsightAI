import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileType, BarChart, PieChart as PieChartIcon } from 'lucide-react';
import { SentimentCounts } from '../types';
import { BarChart as RechartsBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = {
  very_positive: '#4F46E5', // indigo-600
  positive: '#059669',      // green-600
  neutral: '#6B7280',       // gray-500
  negative: '#EA580C',      // orange-600
  very_negative: '#DC2626'  // red-600
};

export default function UploadReviewsPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState<SentimentCounts | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (!['text/csv', 'application/json'].includes(selectedFile.type)) {
        setError('Please upload a CSV or JSON file');
        return;
      }
      setFile(selectedFile);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const endpoint = file.type === 'text/csv' ? '/reviews/import/csv' : '/reviews/import/json';
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to upload file');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Failed to upload and analyze file');
    } finally {
      setLoading(false);
    }
  };

  const prepareChartData = (data: SentimentCounts) => {
    return [
      { name: 'Very Positive', value: data.very_positive, color: COLORS.very_positive },
      { name: 'Positive', value: data.positive, color: COLORS.positive },
      { name: 'Neutral', value: data.neutral, color: COLORS.neutral },
      { name: 'Negative', value: data.negative, color: COLORS.negative },
      { name: 'Very Negative', value: data.very_negative, color: COLORS.very_negative }
    ];
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center space-x-4 mb-6">
              <div className="bg-indigo-100 p-3 rounded-full">
                <Upload className="h-6 w-6 text-indigo-600" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900">Upload Reviews</h3>
                <p className="text-sm text-gray-500">Upload your CSV or JSON file for sentiment analysis</p>
              </div>
            </div>

            {error && (
              <div className="mb-4 bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative">
                {error}
              </div>
            )}

            <div className="mt-4">
              <div className="flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div className="space-y-1 text-center">
                  <FileType className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="flex text-sm text-gray-600">
                    <label
                      htmlFor="file-upload"
                      className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500"
                    >
                      <span>Upload a file</span>
                      <input
                        id="file-upload"
                        name="file-upload"
                        type="file"
                        accept=".csv,.json"
                        className="sr-only"
                        onChange={handleFileChange}
                      />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">CSV or JSON up to 10MB</p>
                </div>
              </div>
            </div>

            {file && (
              <div className="mt-4">
                <p className="text-sm text-gray-500">
                  Selected file: {file.name}
                </p>
                <button
                  onClick={handleUpload}
                  disabled={loading}
                  className="mt-4 w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                  {loading ? 'Analyzing...' : 'Analyze Sentiments'}
                </button>
              </div>
            )}

            {results && (
              <div className="mt-8 space-y-8">
                <div>
                  <h4 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                    <BarChart className="h-5 w-5 mr-2 text-indigo-600" />
                    Analysis Results
                  </h4>
                  <div className="grid grid-cols-2 gap-4 sm:grid-cols-5">
                    <div className="bg-white p-4 rounded-md shadow border border-gray-200">
                      <div className="text-sm font-medium text-gray-500">Very Positive</div>
                      <div className="mt-1 text-2xl font-semibold text-indigo-600">
                        {results.very_positive}
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-md shadow border border-gray-200">
                      <div className="text-sm font-medium text-gray-500">Positive</div>
                      <div className="mt-1 text-2xl font-semibold text-green-600">
                        {results.positive}
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-md shadow border border-gray-200">
                      <div className="text-sm font-medium text-gray-500">Neutral</div>
                      <div className="mt-1 text-2xl font-semibold text-gray-600">
                        {results.neutral}
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-md shadow border border-gray-200">
                      <div className="text-sm font-medium text-gray-500">Negative</div>
                      <div className="mt-1 text-2xl font-semibold text-orange-600">
                        {results.negative}
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-md shadow border border-gray-200">
                      <div className="text-sm font-medium text-gray-500">Very Negative</div>
                      <div className="mt-1 text-2xl font-semibold text-red-600">
                        {results.very_negative}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Bar Chart */}
                  <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                    <h5 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                      <BarChart className="h-5 w-5 mr-2 text-indigo-600"/>
                      Sentiment Distribution
                    </h5>
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <RechartsBarChart
                            data={prepareChartData(results)}
                            margin={{top: 20, right: 30, left: 20, bottom: 5}}
                        >
                          <CartesianGrid strokeDasharray="3 3"/>
                          <XAxis dataKey="name"/>
                          <YAxis/>
                          <Tooltip/>
                          <Legend/>
                          <Bar dataKey="value" name="Count">
                            {prepareChartData(results).map((entry, index) => (
                                <Cell key={index} fill={entry.color}/>
                            ))}
                          </Bar>
                        </RechartsBarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Pie Chart */}
                  <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
                    <h5 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                      <PieChartIcon className="h-5 w-5 mr-2 text-indigo-600"/>
                      Sentiment Proportions
                    </h5>
                    <div className="h-80">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                              data={prepareChartData(results)}
                              cx="50%"
                              cy="50%"
                              labelLine={false}
                              label={({name, percent}) => `${name} (${(percent * 100).toFixed(0)}%)`}
                              outerRadius={80}
                              fill="#8884d8"
                              dataKey="value"
                          >
                            {prepareChartData(results).map((entry, index) => (
                                <Cell key={index} fill={entry.color}/>
                            ))}
                          </Pie>
                          <Tooltip/>
                          <Legend/>
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}