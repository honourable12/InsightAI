import { useState } from "react";
import { changePassword } from "../api";
import "../styles/ChangePassword.css";

function ChangePassword() {
  const [formData, setFormData] = useState({
    current_password: "",
    new_password: "",
  });
  const [status, setStatus] = useState({ type: '', message: '' });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setStatus({ type: '', message: '' });
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      const response = await changePassword(formData, token);
      setStatus({ type: 'success', message: response.data.message });
      setFormData({ current_password: "", new_password: "" });
    } catch (error) {
      console.error(error);
      setStatus({ type: 'error', message: 'Failed to change password' });
    }
  };

  return (
    <div className="password-container">
      <div className="password-card">
        <div className="card-header">
          <h2 className="card-title">Change Password</h2>
          <p className="card-description">
            Update your password to keep your account secure
          </p>
        </div>

        {status.message && (
          <div className={`status-message ${status.type}`}>
            {status.message}
          </div>
        )}

        <form onSubmit={handleChangePassword} className="password-form">
          <div className="form-group">
            <label htmlFor="current_password" className="form-label">
              Current Password
            </label>
            <div className="input-wrapper">
              <input
                type="password"
                name="current_password"
                id="current_password"
                value={formData.current_password}
                onChange={handleChange}
                className="form-input"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="new_password" className="form-label">
              New Password
            </label>
            <div className="input-wrapper">
              <input
                type="password"
                name="new_password"
                id="new_password"
                value={formData.new_password}
                onChange={handleChange}
                className="form-input"
                required
              />
            </div>
          </div>

          <button type="submit" className="submit-button">
            Update Password
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChangePassword;