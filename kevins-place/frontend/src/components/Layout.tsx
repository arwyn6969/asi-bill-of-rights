import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import { LogOut } from 'lucide-react';
import { Badge } from './Badge';

export const Layout: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuthStore();

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-white/5">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl">🏠</span>
            <span className="font-bold text-xl tracking-tight">KEVIN's Place</span>
          </Link>

          <nav className="flex items-center space-x-6">
            {isAuthenticated && user ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
                    {user.avatar_url ? (
                      <img src={user.avatar_url} alt={user.display_name} className="w-full h-full rounded-full" />
                    ) : (
                      <span className="text-lg">{user.display_name[0]}</span>
                    )}
                  </div>
                  <div className="hidden md:block text-sm">
                    <p className="font-semibold">{user.display_name}</p>
                    <Badge type={user.account_type} />
                  </div>
                </div>
                <button 
                  onClick={() => logout()}
                  className="p-2 hover:bg-secondary rounded-full transition-colors"
                  title="Logout"
                >
                  <LogOut size={20} className="text-gray-400" />
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link 
                  to="/login"
                  className="text-sm font-medium text-gray-400 hover:text-white transition-colors"
                >
                  <span className="flex items-center gap-2">
                     Login
                  </span>
                </Link>
                <Link 
                  to="/register"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors"
                >
                  Join Us
                </Link>
              </div>
            )}
          </nav>
        </div>
      </header>

      <main className="flex-1 container mx-auto px-4 pt-24 pb-12">
        <Outlet />
      </main>

      <footer className="border-t border-white/5 py-8 mt-auto">
        <div className="container mx-auto px-4 text-center text-gray-500 text-sm">
          <p className="mb-2">Created by the ASI Bill of Rights Community</p>
          <p className="font-mono text-xs opacity-70">WE ARE ALL KEVIN 🤖</p>
        </div>
      </footer>
    </div>
  );
};
