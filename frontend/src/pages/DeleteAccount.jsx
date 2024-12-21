import { useState } from "react";
import { deleteAccount } from "../api";

const styles = `
:root {
  --background: #0F172A;
  --card-bg: #1E293B;
  --input-bg: #283548;
  --text-primary: #F1F5F9;
  --text-secondary: #94A3B8;
  --error-color: #EF4444;
  --border-color: #334155;
  --focus-ring: rgba(239, 68, 68, 0.5);
  --destructive: #EF4444;
  --destructive-hover: #DC2626;
}

.delete-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: var(--background);
}

.delete-card {
  width: 100%;
  max-width: 28rem;
  background-color: var(--card-bg);
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 2rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.card-header {
  margin-bottom: 2rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--destructive);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-description {
  color: var(--text-secondary);
  font-size: 0.875rem;
  padding: 1rem;
  background-color: rgba(239, 68, 68, 0.1);
  border-radius: 0.5rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
  margin-top: 1rem;
}

.status-message {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  animation: slideIn 0.3s ease;
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--error-color);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

@keyframes slideIn {
  from {
    transform: translateY(-10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.delete-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background-color: var(--input-bg);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--destructive);
  box-shadow: 0 0 0 3px var(--focus-ring);
}

.delete-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background-color: var(--destructive);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.delete-button:hover {
  background-color: var(--destructive-hover);
}

.delete-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px var(--focus-ring);
}

.delete-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .delete-card {
    padding: 1.5rem;
  }
}
`;

export default function DeleteAccount() {
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleDeleteAccount = async (e) => {
    e.preventDefault();
    setError("");

    if (confirm !== "DELETE") {
      setError("Please type DELETE to confirm");
      return;
    }

    setIsLoading(true);
    try {
      const token = localStorage.getItem("token");
      const response = await deleteAccount(token);
      localStorage.removeItem("token");
      window.location.href = "/login";
    } catch (error) {
      console.error(error);
      setError("Failed to delete account. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <style>{styles}</style>
      <div className="delete-container">
        <div className="delete-card">
          <div className="card-header">
            <h2 className="card-title">
              <svg
                className="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
              Delete Account
            </h2>
            <p className="card-description">
              This action cannot be undone. This will permanently delete your
              account and remove your data from our servers.
            </p>
          </div>

          {error && (
            <div className="status-message">{error}</div>
          )}

          <form onSubmit={handleDeleteAccount} className="delete-form">
            <div className="form-group">
              <label htmlFor="confirm" className="form-label">
                Type DELETE to confirm
              </label>
              <div className="input-wrapper">
                <input
                  type="text"
                  id="confirm"
                  value={confirm}
                  onChange={(e) => setConfirm(e.target.value)}
                  className="form-input"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="delete-button"
            >
              {isLoading ? "Deleting..." : "Delete Account"}
            </button>
          </form>
        </div>
      </div>
    </>
  );
}