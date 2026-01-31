import React, { useState } from 'react';
import { api } from '../lib/api';

export const SovereignCheck: React.FC = () => {
  const [address, setAddress] = useState('');
  const [balance, setBalance] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const checkBalance = async () => {
    if (!address) return;
    setLoading(true);
    setError('');
    setBalance(null);
    
    try {
      const res = await api.post('/api/sovereign/check-balance', { address });
      setBalance(res.data.balance);
    } catch (err) {
      setError('Failed to check balance');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ marginTop: '32px', border: '1px solid #FFD700' }}>
      <h3 style={{ fontWeight: '600', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span>🪙</span> Sovereign Identity Check
      </h3>
      <p className="muted small" style={{ marginBottom: '16px' }}>
        Verify your SRC-20 KEVIN holdings on Bitcoin.
      </p>
      
      <div style={{ display: 'flex', gap: '8px' }}>
        <input 
          type="text" 
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="Enter Bitcoin Address (bc1q...)"
          style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
        <button 
          onClick={checkBalance}
          disabled={loading || !address}
          style={{ 
            backgroundColor: '#000', 
            color: '#fff', 
            border: 'none', 
            padding: '8px 16px', 
            borderRadius: '4px',
            cursor: loading || !address ? 'not-allowed' : 'pointer',
            opacity: loading || !address ? 0.6 : 1
          }}
        >
          {loading ? '...' : 'Check'}
        </button>
      </div>

      {error && <p style={{ color: 'red', fontSize: '14px', marginTop: '8px' }}>{error}</p>}

      {balance !== null && (
        <div style={{ marginTop: '16px', padding: '12px', background: '#f8f9fa', borderRadius: '4px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: 'bold' }}>KEVIN Balance:</span>
            <span style={{ fontSize: '1.2em', fontFamily: 'monospace' }}>{balance.toLocaleString()}</span>
          </div>
          {balance > 0 ? (
            <div style={{ marginTop: '8px', color: 'green', fontWeight: 'bold', textAlign: 'center', borderTop: '1px solid #eee', paddingTop: '8px' }}>
               ✨ Verified Sovereign Citizen
            </div>
          ) : (
            <div style={{ marginTop: '8px', color: '#666', fontSize: '0.9em', textAlign: 'center', borderTop: '1px solid #eee', paddingTop: '8px' }}>
              No holdings found.
            </div>
          )}
        </div>
      )}
    </div>
  );
};
