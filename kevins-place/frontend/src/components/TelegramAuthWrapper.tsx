import React, { useEffect, useState } from 'react';
import { useTelegramStore, telegramApi } from '../store/telegram';
import { useAuthStore } from '../store/auth';

export const TelegramAuthWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { setIsInTelegram, setTelegramUser } = useTelegramStore();
  const { login, isAuthenticated } = useAuthStore();
  const [isVerifying, setIsVerifying] = useState(false);

  useEffect(() => {
    // 1. Check if running in Telegram
    if (telegramApi.isInTelegram()) {
      setIsInTelegram(true);
      telegramApi.init(); // Expand and ready
      
      const tgUser = telegramApi.getTelegramUser();
      if (tgUser) {
        setTelegramUser(tgUser);
      }

      // 2. Auto-Login if not authenticated
      if (!isAuthenticated && !isVerifying) {
        verifyTelegramIdentity();
      }
    }
  }, [isAuthenticated]);

  const verifyTelegramIdentity = async () => {
    setIsVerifying(true);
    try {
      const webApp = telegramApi.getWebApp();
      if (!webApp?.initData) return;

      console.log("🔐 Verifying Telegram Identity...");
      const result = await telegramApi.verifyAuth(webApp.initData);
      
      if (result && result.access_token && result.forum_user) {
        console.log("✅ Telegram Auth Success:", result.forum_user.display_name);
        
        // Map backend user to frontend user format if needed
        // The backend returns 'forum_user' inside the result, 
        // but 'login' expects the user object directly.
        // Let's ensure the structure matches what useAuthStore expects.
        // Based on auth.ts: login(user, token)
        
        login(result.forum_user, result.access_token);
      }
    } catch (error) {
      console.error("❌ Telegram Auth Failed:", error);
    } finally {
      setIsVerifying(false);
    }
  };

  if (isVerifying) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-[#FDF8E4]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gold mb-4"></div>
        <p className="font-serif text-lg animate-pulse">Verifying Sovereign Identity...</p>
      </div>
    );
  }

  return <>{children}</>;
};
