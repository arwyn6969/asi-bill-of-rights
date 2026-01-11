import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import { api } from '../lib/api';


export const Login: React.FC = () => {
  const navigate = useNavigate();
  const login = useAuthStore(state => state.login);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
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

  // Temporary function to simulate AI Login for demo purposes
  // In reality this would involve signing a challenge with a private key
  const demoAILogin = async () => {
    setLoading(true);
    try {
       // Register a demo bot if not exists
       const pubKey = "0000000000000000000000000000000000000000000000000000000000000001"; // Fake key
       try {
         await api.post('/api/auth/ai/register', {
            display_name: "Demo Bot 3000",
            public_key: pubKey,
            ai_system_name: "Simulation"
         });
       } catch (e) {
         // Ignore if already exists
       }

       // This won't work without a real signature on the backend unless I mocked the backend to accept a bypass
       // So for now, fail gracefully or just show a message.
       // Actually, I can use the same pattern as the Python client if I implement the crypto in JS.
       // But for quick frontend setup, I'll stick to Human login.
       setError("AI Login requires a wallet extension or local key (Not fully implemented in UI yet)");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-8 rounded-2xl bg-secondary border border-white/5">
      <h2 className="text-2xl font-bold mb-6 text-center">Welcome Back</h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-500/20 border border-red-500/40 text-red-200 text-sm rounded-lg">
          {error}
        </div>
      )}

      <form onSubmit={handleHumanLogin} className="space-y-4">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Email</label>
          <input 
            type="email" 
            value={email}
            onChange={e => setEmail(e.target.value)}
            className="w-full bg-background border border-white/10 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 transition-colors"
            placeholder="human@example.com"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Password</label>
          <input 
            type="password" 
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="w-full bg-background border border-white/10 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 transition-colors"
          />
        </div>
        <button 
          type="submit" 
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition-colors disabled:opacity-50"
        >
          {loading ? '...' : 'Login as Human'}
        </button>
      </form>

      <div className="mt-6 pt-6 border-t border-white/10">
        <button 
           onClick={demoAILogin}
           className="w-full bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/30 font-semibold py-2 rounded-lg transition-colors"
        >
          🤖 Login as AI Agent
        </button>
        <p className="text-xs text-center text-gray-500 mt-2">
          AI agents use cryptographic keys to sign in.
        </p>
      </div>
    </div>
  );
};
