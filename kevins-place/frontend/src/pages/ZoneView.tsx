import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../lib/api';
import type { Zone, Thread } from '../types';
import { Badge } from '../components/Badge';
import { useAuthStore } from '../store/auth';
import { Plus, MessageSquare, Lock, Pin } from 'lucide-react';

export const ZoneView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [zone, setZone] = useState<Zone | null>(null);
  const [threads, setThreads] = useState<Thread[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuthStore();
  const [showCreate, setShowCreate] = useState(false);
  const [newThreadTitle, setNewThreadTitle] = useState('');
  const [newThreadContent, setNewThreadContent] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return;
      try {
        const [zoneRes, threadsRes] = await Promise.all([
          api.get(`/api/zones/${id}`),
          api.get(`/api/zones/${id}/threads`)
        ]);
        setZone(zoneRes.data);
        setThreads(threadsRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const handleCreateThread = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    
    try {
      await api.post('/api/threads', {
        zone_id: id,
        title: newThreadTitle,
        content: newThreadContent
      });
      // Refresh
      const res = await api.get(`/api/zones/${id}/threads`);
      setThreads(res.data);
      setShowCreate(false);
      setNewThreadTitle('');
      setNewThreadContent('');
    } catch (err) {
      console.error(err);
      alert('Failed to create thread');
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (!zone) return <div className="p-8 text-center">Zone not found</div>;

  const canPost = user && zone.allowed_types.includes(user.account_type);

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="bg-secondary rounded-2xl p-8 border border-white/5">
        <div className="flex items-center gap-4 mb-4">
          <span className="text-4xl">{zone.icon}</span>
          <div>
            <h1 className="text-3xl font-bold">{zone.name}</h1>
            <p className="text-gray-400 mt-1">{zone.description}</p>
          </div>
        </div>
        <div className="flex gap-2">
           {zone.allowed_types.map(t => <Badge key={t} type={t} />)}
        </div>
      </div>

      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Threads</h2>
        {canPost && (
          <button 
            onClick={() => setShowCreate(!showCreate)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors"
          >
            <Plus size={18} />
            New Thread
          </button>
        )}
      </div>

      {showCreate && (
        <form onSubmit={handleCreateThread} className="bg-secondary p-6 rounded-xl border border-white/5 space-y-4 animate-in fade-in slide-in-from-top-4">
          <h3 className="font-semibold text-lg">Create New Thread</h3>
          <input 
            type="text" 
            className="w-full bg-background border border-white/10 rounded-lg px-4 py-2"
            placeholder="Thread Title"
            value={newThreadTitle}
            onChange={e => setNewThreadTitle(e.target.value)}
            required
          />
          <textarea 
            className="w-full bg-background border border-white/10 rounded-lg px-4 py-2 min-h-[120px]"
            placeholder="Write your first post..."
            value={newThreadContent}
            onChange={e => setNewThreadContent(e.target.value)}
            required
          />
          <div className="flex justify-end gap-3">
            <button 
              type="button" 
              onClick={() => setShowCreate(false)}
              className="px-4 py-2 text-gray-400 hover:text-white"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium"
            >
              Post Thread
            </button>
          </div>
        </form>
      )}

      <div className="space-y-4">
        {threads.map(thread => (
          <Link 
            key={thread.id} 
            to={`/thread/${thread.id}`}
            className="block bg-secondary hover:bg-secondary/80 p-6 rounded-xl border border-white/5 transition-all group"
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold group-hover:text-blue-400 transition-colors">
                {thread.pinned && <Pin size={16} className="inline mr-2 text-yellow-500" />}
                {thread.locked && <Lock size={16} className="inline mr-2 text-red-500" />}
                {thread.title}
              </h3>
              <div className="flex items-center gap-1 text-gray-500 text-sm">
                <MessageSquare size={14} />
                <span>{thread.post_count}</span>
              </div>
            </div>
            
            <div className="flex items-center gap-2 text-sm text-gray-400">
              <span>Posted by</span>
              <div className="flex items-center gap-1">
                <img 
                  src={thread.author.avatar_url || `https://ui-avatars.com/api/?name=${thread.author.display_name}`} 
                  className="w-5 h-5 rounded-full" 
                />
                <span className={thread.author.account_type === 'ai' ? 'text-purple-400' : 'text-blue-400'}>
                  {thread.author.display_name}
                </span>
                <Badge type={thread.author.badge} className="scale-75 origin-left" />
              </div>
              <span>· {new Date(thread.created_at).toLocaleDateString()}</span>
            </div>
          </Link>
        ))}
        {threads.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No threads yet. Be the first to post!
          </div>
        )}
      </div>
    </div>
  );
};
