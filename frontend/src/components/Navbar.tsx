import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogIn, LogOut, Upload, User as UserIcon } from 'lucide-react';

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className="bg-indigo-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold">
              SentimentAnalyzer
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link
                  to="/upload-reviews"
                  className="flex items-center space-x-1 hover:text-indigo-200 transition-colors"
                >
                  <Upload size={20} />
                  <span>Upload</span>
                </Link>
                <Link
                  to="/profile"
                  className="flex items-center space-x-1 hover:text-indigo-200 transition-colors"
                >
                  <UserIcon size={20} />
                  <span>Profile</span>
                </Link>
                <button
                  onClick={logout}
                  className="flex items-center space-x-1 hover:text-indigo-200 transition-colors"
                >
                  <LogOut size={20} />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="flex items-center space-x-1 hover:text-indigo-200 transition-colors"
                >
                  <LogIn size={20} />
                  <span>Login</span>
                </Link>
                <Link
                  to="/register"
                  className="flex items-center space-x-1 bg-white text-indigo-600 px-4 py-2 rounded-md hover:bg-indigo-50 transition-colors"
                >
                  <span>Sign Up</span>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}