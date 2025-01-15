import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { AuthState, User } from '../types';

interface AuthContextType extends AuthState {
  login: (token: string, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [auth, setAuth] = useState<AuthState>({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
  });

  useEffect(() => {
    if (auth.token) {
      // Validate token and fetch user profile
      fetch('http://localhost:8000/auth/profile', {
        headers: {
          'Authorization': `Bearer ${auth.token}`
        }
      })
      .then(res => res.json())
      .then(user => {
        setAuth(prev => ({
          ...prev,
          user,
          isAuthenticated: true
        }));
      })
      .catch(() => {
        localStorage.removeItem('token');
        setAuth({
          user: null,
          token: null,
          isAuthenticated: false
        });
      });
    }
  }, [auth.token]);

  const login = (token: string, user: User) => {
    localStorage.setItem('token', token);
    setAuth({
      user,
      token,
      isAuthenticated: true
    });
  };

  const logout = () => {
    localStorage.removeItem('token');
    setAuth({
      user: null,
      token: null,
      isAuthenticated: false
    });
  };

  return (
    <AuthContext.Provider value={{ ...auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};