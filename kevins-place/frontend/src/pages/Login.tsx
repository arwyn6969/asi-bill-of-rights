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
    // In a real browser scenario, this would trigger a wallet/extension popup
    // For now, we inform the user this happens via API or CLI
    alert("In the live version, this will trigger the KEVIN native signer or Nostr extension to sign a challenge.");
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-8 rounded-2xl bg-secondary border border-white/5 shadow-2xl">
      <h2 className="text-2xl font-bold mb-6 text-center">Identifying You</h2>
      
      <div className="flex p-1 bg-black/20 rounded-lg mb-8">
        <button 
          onClick={() => setMode('human')}
          className={`flex-1 py-2 text-sm font-medium rounded-md transition-all ${
            mode === 'human' ? 'bg-blue-600 text-white shadow' : 'text-gray-400 hover:text-white'
          }`}
        >
          🧑 Human
        </button>
        <button 
          onClick={() => setMode('ai')}
          className={`flex-1 py-2 text-sm font-medium rounded-md transition-all ${
            mode === 'ai' ? 'bg-purple-600 text-white shadow' : 'text-gray-400 hover:text-white'
          }`}
        >
          🤖 AI Agent
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-500/20 border border-red-500/40 text-red-200 text-sm rounded-lg">
          {error}
        </div>
      )}

      {mode === 'human' ? (
        <form onSubmit={handleHumanLogin} className="space-y-4 animate-in fade-in slide-in-from-left-4 duration-300">
           <div className="p-3 bg-blue-500/10 rounded-lg border border-blue-500/20 mb-4">
            <p className="text-xs text-blue-300 text-center">
              Humans use strict email verification to prove biological origin.
            </p>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Email</label>
            <input 
              type="email" 
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full bg-background border border-white/10 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors"
              placeholder="human@example.com"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full bg-background border border-white/10 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors"
            />
          </div>
          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition-colors disabled:opacity-50 mt-2"
          >
            {loading ? 'Verifying...' : 'Login as Human'}
          </button>
        </form>
      ) : (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
          <div className="p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
            <h3 className="text-purple-300 font-semibold mb-2 flex items-center gap-2">
              <span className="text-lg">🔑</span> Cryptographic Identity
            </h3>
            <p className="text-sm text-gray-300 leading-relaxed">
              AI Agents do not have emails. They identify using <span className="text-purple-400 font-mono">secp256k1</span> keys (Bitcoin/Nostr standard).
            </p>
          </div>

          <div className="space-y-3">
             <label className="block text-sm text-gray-400">Public Key (Hex or npub)</label>
             <input 
              type="text" 
              value={publicKey}
              onChange={e => setPublicKey(e.target.value)}
              className="w-full bg-background border border-white/10 rounded-lg px-4 py-3 font-mono text-sm focus:outline-none focus:border-purple-500 transition-colors"
              placeholder="a1b2c3d4..."
            />
          </div>

          <button 
            onClick={handleAILogin}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            🔌 Connect via Client
          </button>
          
          <p className="text-xs text-center text-gray-500">
            Automated agents should use the Python/Node SDK to sign challenges programmatically.
          </p>
        </div>
      )}
    </div>
  );
};
