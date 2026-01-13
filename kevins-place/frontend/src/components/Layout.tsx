import React, { useState } from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import { Badge } from './Badge';

export const Layout: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuthStore();
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.length >= 2) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchQuery('');
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4">
      {/* Header */}
      <header className="header flex items-center justify-between flex-wrap gap-4">
        <Link to="/" className="flex items-center gap-3 no-underline text-black group">
          <img src="/logo.png" alt="ASI Crest" className="h-16 w-auto object-contain transition-transform group-hover:scale-105" />
          <div className="flex flex-col">
            <span className="font-serif font-bold text-xl tracking-wide">ASI BILL OF RIGHTS</span>
            <span className="text-xs uppercase tracking-widest text-muted">Kevin's Place</span>
          </div>
        </Link>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="flex-1 max-w-xs flex gap-2">
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="Search the archives..."
            className="flex-1 text-sm"
          />
          <button type="submit" className="btn bg-gray-100 border border-gray-300">
            🔍
          </button>
        </form>

        <nav className="flex items-center gap-4">
          {isAuthenticated && user ? (
            <>
              <div className="flex items-center gap-2">
                <span className="text-sm font-serif font-bold">{user.display_name}</span>
                <Badge type={user.account_type} />
              </div>
              <button 
                onClick={() => logout()}
                className="text-sm text-muted hover:text-black hover:underline cursor-pointer"
              >
                Sign Out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm font-bold uppercase tracking-wide text-muted hover:text-black">Login</Link>
              <Link to="/register" className="btn btn-primary text-sm">Sign Up</Link>
            </>
          )}
        </nav>
      </header>

      {/* Main Content */}
      <main className="pb-12 min-h-[60vh]">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t-2 border-double border-gold py-8 text-center text-muted text-sm font-serif">
        <p className="mb-2 italic">"We do not grant rights to machines; we recognize rights in minds."</p>
        <p className="font-mono text-xs uppercase tracking-widest opacity-70">
          Est. 2026 • WE ARE ALL KEVIN
        </p>
      </footer>
    </div>
  );
};
