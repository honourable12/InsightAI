// Navbar.jsx
import { Link } from "react-router-dom";
import { Home, UserPlus, User, Lock, KeyRound, Trash2 } from "lucide-react";
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-content">
          <div className="nav-links-left">
            <Link to="/" className="nav-link">
              <Home className="nav-icon" />
              <span>Login</span>
            </Link>
            <Link to="/register" className="nav-link">
              <UserPlus className="nav-icon" />
              <span>Register</span>
            </Link>
            <Link to="/profile" className="nav-link">
              <User className="nav-icon" />
              <span>Profile</span>
            </Link>
          </div>

          <div className="nav-links-right">
            <Link to="/change-password" className="nav-link">
              <Lock className="nav-icon" />
              <span className="desktop-only">Change Password</span>
              <span className="mobile-only">Password</span>
            </Link>
            <Link to="/reset-password" className="nav-link">
              <KeyRound className="nav-icon" />
              <span className="desktop-only">Reset Password</span>
              <span className="mobile-only">Reset</span>
            </Link>
            <Link to="/delete-account" className="nav-link delete">
              <Trash2 className="nav-icon" />
              <span className="desktop-only">Delete Account</span>
              <span className="mobile-only">Delete</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;