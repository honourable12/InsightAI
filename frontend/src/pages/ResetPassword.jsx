import { useState } from "react";
import { resetPassword } from "../api";
import "../styles/ResetPassword.css";

function ResetPassword() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState({ type: '', message: '' });

  const handleResetPassword = async (e) => {
    e.preventDefault();
    try {
      const response = await resetPassword({ email });
      setStatus({
        type: 'success',
        message: `Temporary password: ${response.data.temp_password}`
      });
      setEmail("");
    } catch (error) {
      console.error(error);
      setStatus({
        type: 'error',
        message: 'Failed to reset password. Please try again.'
      });
    }
  };

  return (
    <div className="reset-container">
      <div className="reset-card">
        <div className="card-header">
          <h2 className="card-title">Reset Password</h2>
          <p className="card-description">
            Enter your email to receive a temporary password
          </p>
        </div>

        {status.message && (
          <div className={`status-message ${status.type}`}>
            {status.message}
          </div>
        )}

        <form onSubmit={handleResetPassword} className="reset-form">
          <div className="form-group">
            <label htmlFor="email" className="form-label">
              Email Address
            </label>
            <div className="input-wrapper">
              <input
                type="email"
                id="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setStatus({ type: '', message: '' });
                }}
                className="form-input"
                required
              />
            </div>
          </div>

          <button type="submit" className="submit-button">
            Reset Password
          </button>
        </form>
      </div>
    </div>
  );
}

export default ResetPassword;