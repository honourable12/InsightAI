import axios from "axios";

const API_URL = "http://localhost:8000";

// Helper function to encode form data
const toFormData = (data) => new URLSearchParams(data);

export const register = (data) =>
  axios.post(
    `${API_URL}/auth/register`,
    new URLSearchParams(data), // Form-encoded data
    {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    }
  );


export const login = (data) =>
  axios.post(`${API_URL}/auth/token`, toFormData(data), {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

export const getProfile = (token) =>
  axios.get(`${API_URL}/auth/profile`, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const changePassword = (data, token) =>
  axios.post(`${API_URL}/auth/change-password`, toFormData(data), {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

export const resetPassword = (data) =>
  axios.post(`${API_URL}/auth/reset-password`, toFormData(data), {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

export const deleteAccount = (token) =>
  axios.delete(`${API_URL}/auth/delete-account`, {
    headers: { Authorization: `Bearer ${token}` },
  });

export const importCsvReviews = (file, token) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios.post(`${API_URL}/reviews/import/csv`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });
};

export const importJsonReviews = (file, token) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios.post(`${API_URL}/reviews/import/json`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });
};

