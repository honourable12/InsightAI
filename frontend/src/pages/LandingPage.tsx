import { Link } from 'react-router-dom';
import { BarChart3, Upload, UserPlus, LogIn } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LandingPage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            Welcome to{' '}
            <span className="text-indigo-600">SentimentAnalyzer</span>
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Your Gateway to Smarter Insights. Upload your reviews and get instant sentiment analysis with powerful visualization tools.
          </p>

          <div className="mt-10">
            {!isAuthenticated ? (
              <div className="space-x-4">
                <Link
                  to="/register"
                  className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  <UserPlus className="mr-2" size={20} />
                  Sign Up
                </Link>
                <Link
                  to="/login"
                  className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50 border-indigo-600"
                >
                  <LogIn className="mr-2" size={20} />
                  Login
                </Link>
              </div>
            ) : (
              <Link
                to="/upload-reviews"
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                <Upload className="mr-2" size={20} />
                Upload Reviews
              </Link>
            )}
          </div>
        </div>

        <div className="mt-20">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="bg-indigo-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                <Upload className="text-indigo-600" size={24} />
              </div>
              <h3 className="text-lg font-medium text-gray-900">Easy Upload</h3>
              <p className="mt-2 text-gray-500">
                Upload your reviews in CSV or JSON format with just a few clicks.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="bg-indigo-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                <BarChart3 className="text-indigo-600" size={24} />
              </div>
              <h3 className="text-lg font-medium text-gray-900">Instant Analysis</h3>
              <p className="mt-2 text-gray-500">
                Get immediate sentiment analysis results with detailed visualizations.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="bg-indigo-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                <UserPlus className="text-indigo-600" size={24} />
              </div>
              <h3 className="text-lg font-medium text-gray-900">User Management</h3>
              <p className="mt-2 text-gray-500">
                Secure user accounts with profile management and password recovery.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}