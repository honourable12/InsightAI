import { useEffect, useState } from "react";
import { getProfile } from "../api";
import "../styles/Profile.css";

function Profile() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await getProfile(token);
        setProfile(response.data);
      } catch (error) {
        console.error(error);
        alert("Failed to fetch profile");
      }
    };
    fetchProfile();
  }, []);

  if (!profile) {
    return (
      <div className="loading-container">
        <p className="loading-text">Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-card">
        <h2 className="profile-title">Profile</h2>
        <div className="profile-fields">
          <div className="profile-field">
            <p className="field-label">Username</p>
            <p className="field-value">{profile.username}</p>
          </div>
          <div className="profile-field">
            <p className="field-label">Email</p>
            <p className="field-value">{profile.email}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;