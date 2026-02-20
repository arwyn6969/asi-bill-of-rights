import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { TelegramState, TelegramStats, TelegramUser, TelegramLinkStatus } from '../types';

const API_URL = import.meta.env.VITE_API_URL || '';

// Extend Window interface for Telegram WebApp
declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        initData: string;
        initDataUnsafe: {
          user?: {
            id: number;
            first_name: string;
            last_name?: string;
            username?: string;
            photo_url?: string;
          };
          auth_date: number;
          hash: string;
        };
        ready: () => void;
        expand: () => void;
        close: () => void;
        MainButton: {
          text: string;
          show: () => void;
          hide: () => void;
          onClick: (callback: () => void) => void;
          setText: (text: string) => void;
        };
        BackButton: {
          show: () => void;
          hide: () => void;
          onClick: (callback: () => void) => void;
        };
        HapticFeedback: {
          impactOccurred: (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') => void;
          notificationOccurred: (type: 'error' | 'success' | 'warning') => void;
          selectionChanged: () => void;
        };
        showAlert: (message: string, callback?: () => void) => void;
        showConfirm: (message: string, callback?: (confirmed: boolean) => void) => void;
        openLink: (url: string, options?: { try_instant_view?: boolean }) => void;
        openTelegramLink: (url: string) => void;
        themeParams: {
          bg_color?: string;
          text_color?: string;
          hint_color?: string;
          link_color?: string;
          button_color?: string;
          button_text_color?: string;
          secondary_bg_color?: string;
        };
        colorScheme: 'light' | 'dark';
        isExpanded: boolean;
        viewportHeight: number;
        viewportStableHeight: number;
      };
    };
  }
}

export const useTelegramStore = create<TelegramState>()(
  persist(
    (set) => ({
      isInTelegram: false,
      telegramUser: null,
      stats: null,
      linkStatus: null,
      isLoading: false,
      error: null,
      setTelegramUser: (user: TelegramUser | null) => set({ telegramUser: user }),
      setStats: (stats: TelegramStats | null) => set({ stats }),
      setLinkStatus: (status: TelegramLinkStatus | null) => set({ linkStatus: status }),
      setIsInTelegram: (isIn: boolean) => set({ isInTelegram: isIn }),
      setLoading: (loading: boolean) => set({ isLoading: loading }),
      setError: (error: string | null) => set({ error }),
    }),
    {
      name: 'telegram-storage',
      partialize: (state) => ({
        // Only persist these fields
        linkStatus: state.linkStatus,
      }),
    }
  )
);

// Telegram API utilities
export const telegramApi = {
  // Check if running inside Telegram WebApp
  isInTelegram: (): boolean => {
    return typeof window !== 'undefined' && 
           !!window.Telegram?.WebApp?.initData;
  },

  // Get Telegram WebApp instance
  getWebApp: () => {
    return window.Telegram?.WebApp;
  },

  // Initialize Telegram WebApp
  init: () => {
    const webApp = window.Telegram?.WebApp;
    if (webApp) {
      webApp.ready();
      webApp.expand();
      return true;
    }
    return false;
  },

  // Get Telegram user info
  getTelegramUser: (): TelegramUser | null => {
    const webApp = window.Telegram?.WebApp;
    const user = webApp?.initDataUnsafe?.user;
    
    if (!user) return null;
    
    return {
      id: String(user.id),
      first_name: user.first_name,
      last_name: user.last_name,
      username: user.username,
      photo_url: user.photo_url,
    };
  },

  // Trigger haptic feedback
  haptic: (type: 'light' | 'medium' | 'heavy' = 'light') => {
    window.Telegram?.WebApp?.HapticFeedback?.impactOccurred(type);
  },

  // Fetch community stats from backend
  fetchStats: async (): Promise<TelegramStats | null> => {
    try {
      const response = await fetch(`${API_URL}/api/telegram/stats`);
      if (!response.ok) throw new Error('Failed to fetch stats');
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch Telegram stats:', error);
      return null;
    }
  },

  // Verify Telegram auth with backend
  verifyAuth: async (initData: string) => {
    try {
      const response = await fetch(`${API_URL}/api/telegram/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ init_data: initData }),
      });
      if (!response.ok) throw new Error('Verification failed');
      return await response.json();
    } catch (error) {
      console.error('Failed to verify Telegram auth:', error);
      return null;
    }
  },

  // Generate link for connecting Telegram account
  generateLink: async (token: string): Promise<{ deep_link: string; auth_token: string; expires_at: string } | null> => {
    try {
      const response = await fetch(`${API_URL}/api/telegram/generate-link`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) throw new Error('Failed to generate link');
      return await response.json();
    } catch (error) {
      console.error('Failed to generate Telegram link:', error);
      return null;
    }
  },

  // Get link status
  getLinkStatus: async (token: string): Promise<TelegramLinkStatus | null> => {
    try {
      const response = await fetch(`${API_URL}/api/telegram/link-status`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) throw new Error('Failed to get link status');
      return await response.json();
    } catch (error) {
      console.error('Failed to get link status:', error);
      return null;
    }
  },

  // Share thread to Telegram
  shareThread: async (threadId: string, token: string, message?: string) => {
    try {
      const response = await fetch(`${API_URL}/api/telegram/share`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ thread_id: threadId, message }),
      });
      if (!response.ok) throw new Error('Failed to generate share link');
      return await response.json();
    } catch (error) {
      console.error('Failed to share thread:', error);
      return null;
    }
  },
};
