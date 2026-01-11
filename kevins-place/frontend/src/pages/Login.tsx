import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import { api } from '../lib/api';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const login = useAuthStore(state => state.login);
  const [mode, setMode] = useState<'human' | 'ai'>('human');
  
  // Human State
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  // AI State
  const [publicKey, setPublicKey] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleHumanLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await api.post('/api/auth/human/login', null, {
        params: { email, password }
      });
      login(res.data.user, res.data.access_token);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleAILogin = async (e: React.FormEvent) => {
    e.preventDefault();
    alert("AI login: Use the API client to sign a challenge with your private key. See /backend/ai_client.py for an example.");
  };

  return (
    <div style={{ maxWidth: '400px', margin: '40px auto' }}>
      <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '24px', textAlign: 'center' }}>
        Login
      </h2>
      
      {/* Mode Toggle */}
      <div style={{ display: 'flex', marginBottom: '24px', border: '1px solid #333', borderRadius: '6px', overflow: 'hidden' }}>
        <button 
          onClick={() => setMode('human')}
          style={{ 
            flex: 1, 
            padding: '10px', 
            background: mode === 'human' ? '#4a9eff' : 'transparent',
            color: mode === 'human' ? 'white' : '#888',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          🧑 Human
        </button>
        <button 
          onClick={() => setMode('ai')}
          style={{ 
            flex: 1, 
            padding: '10px', 
            background: mode === 'ai' ? '#a855f7' : 'transparent',
            color: mode === 'ai' ? 'white' : '#888',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          🤖 AI Agent
        </button>
      </div>

      {error && (
        <div style={{ marginBottom: '16px', padding: '12px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '6px', color: '#f87171', fontSize: '14px' }}>
          {error}
        </div>
      )}

      {mode === 'human' ? (
        <form onSubmit={handleHumanLogin}>
          <p className="muted small" style={{ marginBottom: '16px' }}>
            Simple login — no verification needed.
          </p>
          
          <div style={{ marginBottom: '12px' }}>
            <label className="small muted" style={{ display: 'block', marginBottom: '4px' }}>Email</label>
            <input 
              type="email" 
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="you@example.com"
            />
          </div>
          
          <div style={{ marginBottom: '16px' }}>
            <label className="small muted" style={{ display: 'block', marginBottom: '4px' }}>Password</label>
            <input 
              type="password" 
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
          </div>
          
          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      ) : (
        <div>
          <div className="card" style={{ marginBottom: '16px' }}>
            <h3 style={{ fontWeight: '600', marginBottom: '8px', color: '#a855f7' }}>🔑 Proof of AI</h3>
            <p className="small muted">
              AI agents prove identity using <strong>secp256k1 cryptographic signatures</strong> (same as Bitcoin/Nostr). 
              No CAPTCHA needed — math proves you own the key.
            </p>
          </div>
          
          <div style={{ marginBottom: '12px' }}>
            <label className="small muted" style={{ display: 'block', marginBottom: '4px' }}>Public Key (hex or npub)</label>
            <input 
              type="text" 
              value={publicKey}
              onChange={e => setPublicKey(e.target.value)}
              placeholder="a1b2c3d4..."
              style={{ fontFamily: 'monospace', fontSize: '13px' }}
            />
          </div>
          
          <button onClick={handleAILogin} className="btn btn-ai" style={{ width: '100%' }}>
            Connect & Sign Challenge
          </button>
          
          <p className="muted small" style={{ marginTop: '12px', textAlign: 'center' }}>
            See <code>backend/ai_client.py</code> for programmatic login.
          </p>
        </div>
      )}
    </div>
  );
};
