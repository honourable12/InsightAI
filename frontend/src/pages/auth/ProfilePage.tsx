import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { User, Key, Trash2 } from 'lucide-react';

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setError('New passwords do not match');
      return;
    }

    if (passwordForm.newPassword.length < 8) {
      setError('New password must be at least 8 characters long');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('current_password', passwordForm.currentPassword);
      formData.append('new_password', passwordForm.newPassword);

      const response = await fetch('http://localhost:8000/auth/change-password', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to change password');
      }

      setSuccess('Password changed successfully');
      setIsChangingPassword(false);
      setPasswordForm({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
    } catch (err) {
      setError('Failed to change password');
    }
  };

  const handleDeleteAccount = async () => {
    try {
      const response = await fetch('http://localhost:8000/auth/delete-account', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete account');
      }

      logout();
    } catch (err) {
      setError('Failed to delete account');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center space-x-4 mb-6">
              <div className="bg-indigo-100 p-3 rounded-full">
                <User className="h-6 w-6 text-indigo-600" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900">Profile Information</h3>
                <p className="text-sm text-gray-500">Manage your account settings</p>
              </div>
            </div>

            <div className="border-t border-gray-200 pt-5">
              <dl className="sm:divide-y sm:divide-gray-200">
                <div className="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt className="text-sm font-medium text-gray-500">Username</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {user?.username}
                  </dd>
                </div>
                <div className="py-4 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt className="text-sm font-medium text-gray-500">Email</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {user?.email}
                  </dd>
                </div>
              </dl>
            </div>

            {error && (
              <div className="mt-4 bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative">
                {error}
              </div>
            )}

            {success && (
              <div className="mt-4 bg-green-50 border border-green-400 text-green-700 px-4 py-3 rounded relative">
                {success}
              </div>
            )}

            <div className="mt-6 space-y-4">
              <button
                onClick={() => setIsChangingPassword(!isChangingPassword)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <Key className="mr-2 h-4 w-4" />
                Change Password
              </button>

              {isChangingPassword && (
                <form onSubmit={handlePasswordChange} className="space-y-4">
                  <div>
                    <label htmlFor="currentPassword" className="block text-sm font-medium text-gray-700">
                      Current Password
                    </label>
                    <input
                      type="password"
                      id="currentPassword"
                      value={passwordForm.currentPassword}
                      onChange={(e) => setPasswordForm({ ...passwordForm, currentPassword: e.target.value })}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700">
                      New Password
                    </label>
                    <input
                      type="password"
                      id="newPassword"
                      value={passwordForm.newPassword}
                      onChange={(e) => setPasswordForm({ ...passwordForm, newPassword: e.target.value })}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                      Confirm New Password
                    </label>
                    <input
                      type="password"
                      id="confirmPassword"
                      value={passwordForm.confirmPassword}
                      onChange={(e) => setPasswordForm({ ...passwordForm, confirmPassword: e.target.value })}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                  <button
                    type="submit"
                    className="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Update Password
                  </button>
                </form>
              )}

              <div className="border-t border-gray-200 pt-4">
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  className="inline-flex items-center px-4 py-2 border border-red-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  <Trash2 className="mr-2 h-4 w-4" />
                  Delete Account
                </button>

                {showDeleteConfirm && (
                  <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
                    <div className="bg-white rounded-lg p-6 max-w-sm w-full">
                      <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Delete Account
                      </h3>
                      <p className="text-sm text-gray-500 mb-4">
                        Are you sure you want to delete your account? This action cannot be undone.
                      </p>
                      <div className="flex justify-end space-x-4">
                        <button
                          onClick={() => setShowDeleteConfirm(false)}
                          className="inline-flex justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={handleDeleteAccount}
                          className="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}