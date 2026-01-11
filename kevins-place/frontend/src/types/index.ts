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

// Telegram types
export interface TelegramStats {
  member_count: number;
  online_count: number;
  bot_name: string;
  channel_name: string;
  last_updated: string;
}

export interface TelegramUser {
  id: string;
  username?: string;
  first_name?: string;
  last_name?: string;
  photo_url?: string;
}

export interface TelegramLinkStatus {
  linked: boolean;
  telegram_id?: string;
  telegram_username?: string;
  linked_at?: string;
}

export interface TelegramAuthResponse {
  authenticated: boolean;
  linked: boolean;
  telegram_id?: string;
  telegram_username?: string;
  telegram_first_name?: string;
  forum_user?: {
    id: string;
    display_name: string;
    account_type: AccountType;
    badge: string;
  };
  access_token?: string;
}

export interface ShareToTelegramResponse {
  share_url: string;
  copy_text: string;
  thread_title: string;
}

export interface TelegramState {
  isInTelegram: boolean;
  telegramUser: TelegramUser | null;
  stats: TelegramStats | null;
  linkStatus: TelegramLinkStatus | null;
  isLoading: boolean;
  error: string | null;
  setTelegramUser: (user: TelegramUser | null) => void;
  setStats: (stats: TelegramStats | null) => void;
  setLinkStatus: (status: TelegramLinkStatus | null) => void;
  setIsInTelegram: (isIn: boolean) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

