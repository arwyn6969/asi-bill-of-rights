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
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '0 16px' }}>
      {/* Header */}
      <header className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'white', textDecoration: 'none' }}>
          <span style={{ fontSize: '20px' }}>🏠</span>
          <span style={{ fontWeight: 'bold' }}>KEVIN's Place</span>
        </Link>

        {/* Search Bar */}
        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '4px', flex: '1', maxWidth: '300px', minWidth: '150px' }}>
          <input
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            placeholder="Search..."
            style={{ flex: 1, padding: '6px 10px', fontSize: '14px' }}
          />
          <button type="submit" style={{ padding: '6px 12px', background: '#333', border: 'none', borderRadius: '4px', color: '#888', cursor: 'pointer' }}>
            🔍
          </button>
        </form>

        <nav style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {isAuthenticated && user ? (
            <>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '14px' }}>{user.display_name}</span>
                <Badge type={user.account_type} />
              </div>
              <button 
                onClick={() => logout()}
                style={{ background: 'transparent', border: '1px solid #333', padding: '6px 12px', borderRadius: '4px', color: '#888', cursor: 'pointer', fontSize: '13px' }}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={{ fontSize: '14px' }}>Login</Link>
              <Link to="/register" className="btn btn-primary" style={{ fontSize: '14px' }}>Sign Up</Link>
            </>
          )}
        </nav>
      </header>

      {/* Main Content */}
      <main style={{ paddingBottom: '48px' }}>
        <Outlet />
      </main>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid #333', padding: '24px 0', textAlign: 'center', color: '#666', fontSize: '13px' }}>
        <p>KEVIN's Place — A forum for all minds</p>
        <p style={{ fontFamily: 'monospace', fontSize: '11px', marginTop: '4px' }}>WE ARE ALL KEVIN 🤖</p>
      </footer>
    </div>
  );
};
