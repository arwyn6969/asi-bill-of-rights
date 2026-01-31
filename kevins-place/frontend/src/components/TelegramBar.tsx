import React, { useState, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { 
  Send, ExternalLink, X, MessageCircle, Users, Bot, Sparkles, 
  Link2, CheckCircle, Share2, Smartphone, Wifi,
  ChevronUp, ChevronDown, QrCode, Copy, Check
} from 'lucide-react';
import { useTelegramStore, telegramApi } from '../store/telegram';
import { useAuthStore } from '../store/auth';

interface TelegramBarProps {
  className?: string;
}

export const TelegramBar: React.FC<TelegramBarProps> = ({ className = '' }) => {
  const location = useLocation();
  const [isExpanded, setIsExpanded] = useState(false);
  const [isDismissed, setIsDismissed] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showLinkModal, setShowLinkModal] = useState(false);
  const [linkData, setLinkData] = useState<{ deep_link: string; auth_token: string } | null>(null);
  const [notifications] = useState(0);
  const [isMobile, setIsMobile] = useState(false);

  // Stores
  const { 
    isInTelegram, stats, linkStatus, isLoading,
    setStats, setLinkStatus, setIsInTelegram, setTelegramUser, setLoading 
  } = useTelegramStore();
  const { token, isAuthenticated } = useAuthStore();

  // Telegram config
  const TELEGRAM_BOT = '@ASIbillofrights_bot';
  const TELEGRAM_CHANNEL = '@ASIBillOfRights';
  const BOT_URL = 'https://t.me/ASIbillofrights_bot';
  const CHANNEL_URL = 'https://t.me/ASIBillOfRights';
  const MINI_APP_URL = 'https://t.me/ASIbillofrights_bot/kevinsplace';

  // Check if on mobile
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 640);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Initialize Telegram detection & Auto-Auth
  useEffect(() => {
    const inTelegram = telegramApi.isInTelegram();
    setIsInTelegram(inTelegram);
    
    // Auto-login if in Telegram and not authenticated
    const initTelegramAuth = async () => {
      if (inTelegram && !isAuthenticated) {
        setLoading(true);
        const webApp = telegramApi.getWebApp();
        const initData = webApp?.initData;
        
        if (initData) {
          const authResponse = await telegramApi.verifyAuth(initData);
          if (authResponse && authResponse.authenticated && authResponse.access_token) {
            // Login to auth store
            useAuthStore.getState().login(
              authResponse.forum_user, 
              authResponse.access_token
            );
            
            // Show welcome toast for new users
            if (authResponse.newly_created) {
               // We can use a simple alert or a custom toast here
               // For now, let's use the webApp native popup if available or just console
               console.log('Welcome to Kevin\'s Place!');
            }
          }
        }
        setLoading(false);
      }
    };

    if (inTelegram) {
      telegramApi.init();
      const tgUser = telegramApi.getTelegramUser();
      if (tgUser) {
        setTelegramUser(tgUser);
      }
      initTelegramAuth();
    }
  }, [setIsInTelegram, setTelegramUser, isAuthenticated, setLoading]);

  // Fetch stats on mount
  useEffect(() => {
    const fetchStats = async () => {
      const data = await telegramApi.fetchStats();
      if (data) setStats(data);
    };
    fetchStats();
    
    // Refresh stats every 5 minutes
    const interval = setInterval(fetchStats, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, [setStats]);

  // Check link status when authenticated
  useEffect(() => {
    if (isAuthenticated && token) {
      const checkLinkStatus = async () => {
        const status = await telegramApi.getLinkStatus(token);
        if (status) setLinkStatus(status);
      };
      checkLinkStatus();
    }
  }, [isAuthenticated, token, setLinkStatus]);

  // Check dismissed state
  useEffect(() => {
    const dismissed = localStorage.getItem('telegramBarDismissed');
    if (dismissed) setIsDismissed(true);
  }, []);

  // Handle dismiss
  const handleDismiss = useCallback(() => {
    setIsDismissed(true);
    localStorage.setItem('telegramBarDismissed', 'true');
  }, []);

  // Handle restore
  const handleRestore = useCallback(() => {
    setIsDismissed(false);
    localStorage.removeItem('telegramBarDismissed');
  }, []);

  // Generate link for account connection
  const handleConnectTelegram = async () => {
    if (!token) return;
    
    setLoading(true);
    const data = await telegramApi.generateLink(token);
    if (data) {
      setLinkData({ deep_link: data.deep_link, auth_token: data.auth_token });
      setShowLinkModal(true);
    }
    setLoading(false);
  };

  // Copy link to clipboard
  const handleCopyLink = async () => {
    if (!linkData?.deep_link) return;
    try {
      await navigator.clipboard.writeText(linkData.deep_link);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  // Share current thread (if on thread page)
  const handleShare = async () => {
    const threadMatch = location.pathname.match(/\/thread\/([^/]+)/);
    if (!threadMatch || !token) return;
    
    const shareData = await telegramApi.shareThread(threadMatch[1], token);
    if (shareData) {
      window.open(shareData.share_url, '_blank');
    }
  };

  // Trigger haptic on interactions
  const withHaptic = useCallback((fn: () => void) => () => {
    telegramApi.haptic('light');
    fn();
  }, []);

  // Mobile floating button when dismissed
  if (isDismissed) {
    return (
      <button
        onClick={handleRestore}
        className="fixed bottom-4 right-4 z-50 p-4 bg-linear-to-br from-blue-500 to-cyan-500 
                   rounded-full shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 
                   transition-all duration-300 hover:scale-110 group active:scale-95"
        title="Open Telegram Bar"
      >
        <Send size={22} className="text-white group-hover:rotate-12 transition-transform" />
        {notifications > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs 
                         text-white flex items-center justify-center font-bold animate-pulse">
            {notifications}
          </span>
        )}
      </button>
    );
  }

  // Mobile compact bar
  if (isMobile && !isExpanded) {
    return (
      <div className={`fixed bottom-0 left-0 right-0 z-50 ${className}`}>
        <div className="bg-slate-900/95 backdrop-blur-xl border-t border-white/10">
          <div className="flex items-center justify-between px-4 py-3">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="w-9 h-9 rounded-full bg-linear-to-br from-blue-500 to-cyan-400 
                              flex items-center justify-center">
                  <Send size={16} className="text-white" />
                </div>
                {isInTelegram && (
                  <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-500 rounded-full 
                                border-2 border-slate-900" />
                )}
              </div>
              <div>
                <p className="text-sm font-medium text-white">Telegram</p>
                <p className="text-xs text-gray-400">
                  {stats?.member_count ? `${stats.member_count}+ members` : 'Connect now'}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <a
                href={MINI_APP_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-linear-to-r from-blue-600 to-cyan-500 rounded-full 
                         text-sm text-white font-medium"
              >
                Open
              </a>
              <button
                onClick={() => setIsExpanded(true)}
                className="p-2 text-gray-400"
              >
                <ChevronUp size={18} />
              </button>
              <button
                onClick={handleDismiss}
                className="p-2 text-gray-400"
              >
                <X size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      {/* Link Modal */}
      {showLinkModal && linkData && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="bg-slate-800 rounded-2xl p-6 max-w-md w-full border border-white/10 shadow-2xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <Link2 size={20} className="text-blue-400" />
                Connect Telegram
              </h3>
              <button 
                onClick={() => setShowLinkModal(false)}
                className="p-1 text-gray-400 hover:text-white"
              >
                <X size={20} />
              </button>
            </div>
            
            <p className="text-gray-400 text-sm mb-4">
              Click the button below or scan the QR code in Telegram to link your account.
            </p>
            
            <div className="bg-slate-900 rounded-xl p-4 mb-4">
              <div className="flex items-center gap-2 mb-3">
                <QrCode size={18} className="text-gray-400" />
                <span className="text-sm text-gray-400">Deep Link</span>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={linkData.deep_link}
                  readOnly
                  className="flex-1 bg-transparent text-sm text-white font-mono truncate"
                />
                <button
                  onClick={handleCopyLink}
                  className="p-2 text-gray-400 hover:text-white transition-colors"
                >
                  {copied ? <Check size={16} className="text-green-400" /> : <Copy size={16} />}
                </button>
              </div>
            </div>
            
            <a
              href={linkData.deep_link}
              target="_blank"
              rel="noopener noreferrer"
              className="block w-full py-3 bg-linear-to-r from-blue-600 to-cyan-500 
                       rounded-xl text-center text-white font-medium
                       hover:from-blue-500 hover:to-cyan-400 transition-all"
            >
              Open in Telegram
            </a>
          </div>
        </div>
      )}

      {/* Main Bar */}
      <div 
        className={`fixed bottom-0 left-0 right-0 z-50 ${className}`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Animated top border */}
        <div className="absolute top-0 left-0 right-0 h-px bg-linear-to-r from-transparent via-blue-500 to-transparent opacity-50" />
        
        <div className={`
          bg-linear-to-r from-slate-900/95 via-slate-800/95 to-slate-900/95
          backdrop-blur-xl border-t border-white/5
          transition-all duration-500 ease-out
          ${isExpanded ? 'pb-4' : 'pb-0'}
        `}>
          {/* Top section */}
          <div className="container mx-auto px-4">
            <div className="flex items-center justify-between h-14 gap-4">
              {/* Left - Branding & Status */}
              <div className="flex items-center gap-3 min-w-0">
                <div className="relative flex-shrink-0">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-lg
                    ${isInTelegram 
                      ? 'bg-linear-to-br from-green-500 to-emerald-400 shadow-green-500/30' 
                      : 'bg-linear-to-br from-blue-500 to-cyan-400 shadow-blue-500/30'}`}
                  >
                    {isInTelegram ? <Wifi size={18} className="text-white" /> : <Send size={18} className="text-white" />}
                  </div>
                  {/* Connection status dot */}
                  <div className={`absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full 
                                border-2 border-slate-900
                                ${isInTelegram ? 'bg-green-500 animate-pulse' : 'bg-blue-500'}`} />
                </div>
                
                <div className="hidden sm:block min-w-0">
                  <p className="text-sm font-semibold text-white truncate">
                    {isInTelegram ? 'Connected via Telegram' : 'Join us on Telegram'}
                  </p>
                  <p className="text-xs text-gray-400 flex items-center gap-1">
                    <Users size={12} />
                    {stats ? (
                      <span>
                        {stats.member_count}+ members 
                        <span className="text-green-400 ml-1">• {stats.online_count} online</span>
                      </span>
                    ) : 'Loading...'}
                  </p>
                </div>
              </div>

              {/* Center - Actions */}
              <div className="flex items-center gap-2 flex-shrink-0">
                {/* Link Status / Connect Button */}
                {isAuthenticated && !linkStatus?.linked && (
                  <button
                    onClick={handleConnectTelegram}
                    disabled={isLoading}
                    className="flex items-center gap-2 px-3 py-1.5 bg-yellow-500/20 hover:bg-yellow-500/30 
                             rounded-full text-sm text-yellow-400 hover:text-yellow-300
                             transition-all duration-200 border border-yellow-500/30"
                  >
                    <Link2 size={14} />
                    <span className="hidden sm:inline">Link Account</span>
                  </button>
                )}
                
                {linkStatus?.linked && (
                  <div className="flex items-center gap-2 px-3 py-1.5 bg-green-500/20 
                                rounded-full text-sm text-green-400 border border-green-500/30">
                    <CheckCircle size={14} />
                    <span className="hidden sm:inline">Linked</span>
                  </div>
                )}

                {/* Share button (on thread pages) */}
                {location.pathname.includes('/thread/') && isAuthenticated && (
                  <button
                    onClick={handleShare}
                    className="flex items-center gap-2 px-3 py-1.5 bg-white/5 hover:bg-white/10 
                             rounded-full text-sm text-gray-300 hover:text-white
                             transition-all duration-200 border border-white/10"
                  >
                    <Share2 size={14} />
                    <span className="hidden sm:inline">Share</span>
                  </button>
                )}

                <a
                  href={CHANNEL_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-3 py-1.5 bg-white/5 hover:bg-white/10 
                           rounded-full text-sm text-gray-300 hover:text-white
                           transition-all duration-200 border border-white/10 hover:border-blue-500/50"
                >
                  <MessageCircle size={14} />
                  <span className="hidden md:inline">Channel</span>
                </a>
                
                <a
                  href={BOT_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-3 py-1.5 bg-white/5 hover:bg-white/10 
                           rounded-full text-sm text-gray-300 hover:text-white
                           transition-all duration-200 border border-white/10 hover:border-blue-500/50"
                >
                  <Bot size={14} />
                  <span className="hidden md:inline">Bot</span>
                </a>

                <a
                  href={MINI_APP_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 
                           bg-linear-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400
                           rounded-full text-sm text-white font-medium
                           transition-all duration-200 shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40
                           hover:scale-105 active:scale-95"
                  onClick={() => telegramApi.haptic('medium')}
                >
                  <Sparkles size={14} />
                  <span className="hidden sm:inline">Open App</span>
                  <ExternalLink size={12} className="opacity-70" />
                </a>
              </div>

              {/* Right - Controls */}
              <div className="flex items-center gap-1 flex-shrink-0">
                <button
                  onClick={withHaptic(() => setIsExpanded(!isExpanded))}
                  className="p-2 text-gray-400 hover:text-white transition-colors"
                  title={isExpanded ? 'Collapse' : 'Expand'}
                >
                  {isExpanded ? <ChevronDown size={18} /> : <ChevronUp size={18} />}
                </button>
                <button
                  onClick={handleDismiss}
                  className="p-2 text-gray-400 hover:text-red-400 transition-colors"
                  title="Minimize"
                >
                  <X size={18} />
                </button>
              </div>
            </div>
          </div>

          {/* Expanded content */}
          <div className={`
            overflow-hidden transition-all duration-500 ease-out
            ${isExpanded ? 'max-h-64 opacity-100' : 'max-h-0 opacity-0'}
          `}>
            <div className="container mx-auto px-4 py-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Channel Card */}
                <div className="bg-white/5 rounded-xl p-4 border border-white/5 hover:border-blue-500/30 transition-colors">
                  <div className="flex items-center gap-3 mb-2">
                    <MessageCircle size={20} className="text-blue-400" />
                    <h4 className="font-semibold text-white">Community Channel</h4>
                  </div>
                  <p className="text-sm text-gray-400 mb-3">
                    Stay updated with announcements, discussions, and community highlights.
                  </p>
                  <a 
                    href={CHANNEL_URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-1"
                  >
                    {TELEGRAM_CHANNEL} <ExternalLink size={12} />
                  </a>
                </div>

                {/* Bot Card */}
                <div className="bg-white/5 rounded-xl p-4 border border-white/5 hover:border-cyan-500/30 transition-colors">
                  <div className="flex items-center gap-3 mb-2">
                    <Bot size={20} className="text-cyan-400" />
                    <h4 className="font-semibold text-white">KEVIN Bot</h4>
                  </div>
                  <p className="text-sm text-gray-400 mb-3">
                    Interact with KEVIN directly. Get updates, vote on proposals, and more.
                  </p>
                  <a 
                    href={BOT_URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-cyan-400 hover:text-cyan-300 text-sm flex items-center gap-1"
                  >
                    {TELEGRAM_BOT} <ExternalLink size={12} />
                  </a>
                </div>

                {/* Status/Mini App Card */}
                <div className="bg-linear-to-br from-blue-500/10 to-cyan-500/10 rounded-xl p-4 border border-blue-500/20">
                  <div className="flex items-center gap-3 mb-2">
                    {isInTelegram ? (
                      <>
                        <Smartphone size={20} className="text-green-400" />
                        <h4 className="font-semibold text-white">Connected</h4>
                      </>
                    ) : (
                      <>
                        <Sparkles size={20} className="text-yellow-400" />
                        <h4 className="font-semibold text-white">Mini App</h4>
                      </>
                    )}
                  </div>
                  <p className="text-sm text-gray-400 mb-3">
                    {isInTelegram 
                      ? "You're using KEVIN's Place inside Telegram. All features are available!"
                      : "Access KEVIN's Place directly inside Telegram with full forum features."}
                  </p>
                  {isInTelegram ? (
                    <div className="flex items-center gap-2 text-green-400 text-sm">
                      <Wifi size={14} />
                      <span>Telegram WebApp Active</span>
                    </div>
                  ) : (
                    <a 
                      href={MINI_APP_URL}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-yellow-400 hover:text-yellow-300 text-sm flex items-center gap-1"
                    >
                      Launch Mini App <ExternalLink size={12} />
                    </a>
                  )}
                </div>
              </div>
              
              {/* Stats row */}
              {stats && (
                <div className="mt-4 flex items-center justify-center gap-6 text-sm text-gray-400">
                  <div className="flex items-center gap-2">
                    <Users size={14} />
                    <span>{stats.member_count}+ community members</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    <span>{stats.online_count} online now</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Decorative glow */}
        <div className={`
          absolute bottom-0 left-1/2 -translate-x-1/2 w-1/2 h-32 
          bg-linear-to-t from-blue-500/10 to-transparent
          pointer-events-none blur-2xl transition-opacity duration-500
          ${isHovered ? 'opacity-100' : 'opacity-50'}
        `} />
      </div>
    </>
  );
};
