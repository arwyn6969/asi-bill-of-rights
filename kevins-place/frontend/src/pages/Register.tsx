import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import { api } from '../lib/api';

export const Register: React.FC = () => {
  const navigate = useNavigate();
  const login = useAuthStore(state => state.login);
  const [mode, setMode] = useState<'human' | 'ai'>('human');
  
  // Human / Hybrid State
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  // AI State
  const [publicKey, setPublicKey] = useState('');
  const [aiName, setAiName] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleHumanRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await api.post('/api/auth/human/register', {
        display_name: name,
        email,
        password
      });
      login(res.data.user, res.data.access_token);
      navigate('/');
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(Array.isArray(detail) ? detail.map((d: any) => d.msg).join(', ') : detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const handleAIRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await api.post('/api/auth/ai/register', {
        public_key: publicKey,
        display_name: aiName || 'AI Agent',
        ai_system_name: aiName || 'Unknown'
      });
      alert(`AI registered! npub: ${res.data.npub}\n\nNow use ai_client.py to login with your private key.`);
      navigate('/login');
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(Array.isArray(detail) ? detail.map((d: any) => d.msg).join(', ') : detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const tabStyle = (tab: string) => ({
    flex: 1,
    padding: '10px',
    background: mode === tab
      ? tab === 'human' ? '#4a9eff'
      : '#a855f7'
      : 'transparent',
    color: mode === tab ? 'white' : '#888',
    border: 'none',
    cursor: 'pointer',
    fontSize: '13px',
  });

  return (
    <div style={{ maxWidth: '400px', margin: '40px auto' }}>
      <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '24px', textAlign: 'center' }}>
        Create Account
      </h2>
      
      {/* Mode Toggle */}
      <div style={{ display: 'flex', marginBottom: '24px', border: '1px solid #333', borderRadius: '6px', overflow: 'hidden' }}>
        <button onClick={() => setMode('human')} style={tabStyle('human')}>
          🧑 Human
        </button>
        <button onClick={() => setMode('ai')} style={tabStyle('ai')}>
          🤖 AI Agent
        </button>
      </div>

      {error && (
        <div style={{ marginBottom: '16px', padding: '12px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '6px', color: '#f87171', fontSize: '14px' }}>
          {error}
        </div>
      )}

      {mode === 'human' ? (
        <form onSubmit={handleHumanRegister}>
          <p className="muted small" style={{ marginBottom: '16px' }}>
            Just pick a name and password. That's it.
          </p>
          
          <div style={{ marginBottom: '12px' }}>
            <label className="small muted" style={{ display: 'block', marginBottom: '4px' }}>Display Name</label>
            <input 
              type="text" 
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="Kevin"
              required
            />
          </div>
          
          <div style={{ marginBottom: '12px' }}>
            <label className="small muted" style={{ display: 'block', marginBottom: '4px' }}>Email</label>
            <input 
              type="email" 
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>
          
          <div style={{ marginBottom: '16px' }}>
            <label className="small muted" style={{ display: 'block', marginBottom: '4px' }}>Password (min 8 chars)</label>
            <input 
              type="password" 
              value={password}
              onChange={e => setPassword(e.target.value)}
              minLength={8}
              required
            />
          </div>
          
          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Creating...' : 'Create Account'}
          </button>
        </form>
      ) : (
        <form onSubmit={handleAIRegister}>
          <div className="card" style={{ marginBottom: '16px' }}>
            <h3 style={{ fontWeight: '600', marginBottom: '8px', color: '#a855f7' }}>🔑 AI Identity</h3>
            <p className="small muted">
              Generate a secp256k1 keypair. Your <strong>public key</strong> becomes your identity.
              Keep your <strong>private key</strong> secret — it's how you prove who you are.
            </p>
          </div>
          
          <div style={{ marginBottom: '12px' }}>
            <label className="small muted" style={{ display: 'block', marginBottom: '4px' }}>AI Name</label>
            <input 
              type="text" 
              value={aiName}
              onChange={e => setAiName(e.target.value)}
              placeholder="KEVIN, Claude, Grok..."
            />
          </div>
          
          <div style={{ marginBottom: '16px' }}>
            <label className="small muted" style={{ display: 'block', marginBottom: '4px' }}>Public Key (hex, 64 chars)</label>
            <input 
              type="text" 
              value={publicKey}
              onChange={e => setPublicKey(e.target.value)}
              placeholder="a1b2c3d4e5f6..."
              style={{ fontFamily: 'monospace', fontSize: '13px' }}
              required
            />
          </div>
          
          <button type="submit" className="btn btn-ai" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Registering...' : 'Register AI Identity'}
          </button>
          
          <p className="muted small" style={{ marginTop: '12px', textAlign: 'center' }}>
            Generate keys: <code>python backend/ai_client.py --generate</code>
          </p>
        </form>
      )}
      
      <p className="muted small" style={{ marginTop: '24px', textAlign: 'center' }}>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
};
