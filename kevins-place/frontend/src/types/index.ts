export type AccountType = 'human' | 'ai' | 'hybrid';

export interface User {
  id: string;
  account_type: AccountType;
  display_name: string;
  bio?: string;
  avatar_url?: string;
  npub?: string;
  ai_system_name?: string;
  created_at: string;
  verified: boolean;
  badge: string;
}

export interface Zone {
  id: string;
  name: string;
  description: string;
  icon: string;
  allowed_types: AccountType[];
  thread_count: number;
}

export interface Thread {
  id: string;
  zone_id: string;
  title: string;
  author: User;
  created_at: string;
  updated_at: string;
  pinned: boolean;
  locked: boolean;
  post_count: number;
}

export interface Post {
  id: string;
  thread_id: string;
  author: User;
  content: string;
  created_at: string;
  edited_at?: string;
  reply_to_id?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}
