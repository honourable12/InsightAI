export interface User {
  username: string;
  email: string | null;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface SentimentCounts {
  very_positive: number;
  positive: number;
  neutral: number;
  negative: number;
  very_negative: number;
}