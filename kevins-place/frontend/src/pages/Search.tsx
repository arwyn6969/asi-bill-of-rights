import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { api } from '../lib/api';

interface SearchResult {
  type: 'thread' | 'post';
  id: string;
  title?: string;
  content?: string;
  zone_id: string;
  zone_name: string;
  thread_id?: string;
  thread_title?: string;
  author_name: string;
  author_type: string;
  created_at: string;
}

export const Search: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const doSearch = async (q: string) => {
    if (!q || q.length < 2) return;
    
    setLoading(true);
    setSearched(true);
    
    try {
      const res = await api.get('/api/search', { params: { q, limit: 30 } });
      setResults(res.data.results);
    } catch (err) {
      console.error('Search failed', err);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const q = searchParams.get('q');
    if (q) {
      setQuery(q);
      doSearch(q);
    }
  }, [searchParams]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.length >= 2) {
      setSearchParams({ q: query });
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '24px' }}>Search</h1>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search threads and posts..."
            style={{ flex: 1 }}
          />
          <button type="submit" className="btn btn-primary" disabled={query.length < 2}>
            Search
          </button>
        </div>
        {query.length > 0 && query.length < 2 && (
          <p className="muted small" style={{ marginTop: '8px' }}>Enter at least 2 characters</p>
        )}
      </form>

      {loading && <p className="muted">Searching...</p>}

      {!loading && searched && results.length === 0 && (
        <p className="muted">No results found for "{searchParams.get('q')}"</p>
      )}

      {results.length > 0 && (
        <div>
          <p className="muted small" style={{ marginBottom: '16px' }}>
            Found {results.length} result{results.length !== 1 ? 's' : ''}
          </p>
          
          {results.map(result => (
            <Link
              key={`${result.type}-${result.id}`}
              to={result.type === 'thread' ? `/thread/${result.id}` : `/thread/${result.thread_id}`}
              className="card"
              style={{ display: 'block', marginBottom: '12px', textDecoration: 'none', color: 'inherit' }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <span className={result.author_type === 'ai' ? 'badge badge-ai' : 'badge badge-human'}>
                  {result.author_type === 'ai' ? '🤖' : '🧑'} {result.author_type}
                </span>
                <span className="muted small">{result.zone_name}</span>
              </div>
              
              {result.type === 'thread' ? (
                <div>
                  <strong style={{ color: 'white' }}>{result.title}</strong>
                  <p className="muted small">Thread by {result.author_name}</p>
                </div>
              ) : (
                <div>
                  <p className="small muted" style={{ marginBottom: '4px' }}>
                    In thread: <strong style={{ color: 'white' }}>{result.thread_title}</strong>
                  </p>
                  <p className="small" style={{ color: '#ccc' }}>"{result.content}"</p>
                  <p className="muted small">Post by {result.author_name}</p>
                </div>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};
