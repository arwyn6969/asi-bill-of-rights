import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../lib/api';
import type { Thread, Post, Zone } from '../types';
import { Badge } from '../components/Badge';
import { useAuthStore } from '../store/auth';
import { ArrowLeft, Send, ShieldCheck, Lock } from 'lucide-react';

export const ThreadView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [thread, setThread] = useState<Thread | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [zone, setZone] = useState<Zone | null>(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuthStore();
  const [newPost, setNewPost] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return;
      try {
        const res = await api.get(`/api/threads/${id}`);
        setThread(res.data.thread);
        setPosts(res.data.posts);
        
        // Fetch zone info for permissions
        const zoneRes = await api.get(`/api/zones/${res.data.thread.zone_id}`);
        setZone(zoneRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const handlePost = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !newPost.trim()) return;

    try {
      await api.post(`/api/threads/${id}/posts`, {
        content: newPost
      });
      // Refresh
      const res = await api.get(`/api/threads/${id}`);
      setThread(res.data.thread);
      setPosts(res.data.posts);
      setNewPost('');
    } catch (err) {
      console.error(err);
      alert('Failed to post reply');
    }
  };

  if (loading) return <div className="p-8 text-center animate-pulse">Loading discussion...</div>;
  if (!thread) return <div className="p-8 text-center">Thread not found</div>;

  const canPost = user && zone && zone.allowed_types.includes(user.account_type) && !thread.locked;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Link to={`/zone/${thread.zone_id}`} className="inline-flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
        <ArrowLeft size={16} />
        Back to {zone?.name || 'Zone'}
      </Link>

      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2 flex items-center gap-2">
          {thread.title}
          {thread.locked && <Lock size={24} className="text-red-500" />}
        </h1>
      </div>

      <div className="space-y-6">
        {posts.map((post, index) => (
          <div key={post.id} className={`flex gap-4 ${index === 0 ? 'bg-secondary/50 p-6 rounded-2xl border border-white/5' : ''}`}>
             <div className="flex-shrink-0">
               <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center overflow-hidden">
                 {post.author.avatar_url ? (
                   <img src={post.author.avatar_url} alt="" className="w-full h-full object-cover" />
                 ) : (
                   <span>{post.author.display_name[0]}</span>
                 )}
               </div>
             </div>
             <div className="flex-1 space-y-2">
               <div className="flex items-center gap-2">
                 <span className="font-semibold text-lg">{post.author.display_name}</span>
                 <Badge type={post.author.account_type as 'human' | 'ai' | 'hybrid'} />
                 <span className="text-gray-500 text-sm ml-auto">
                   {new Date(post.created_at).toLocaleString()}
                 </span>
               </div>
               
               <div className="prose prose-invert max-w-none text-gray-300">
                 <p className="whitespace-pre-wrap leading-relaxed">{post.content}</p>
               </div>

               {post.author.account_type === 'ai' && (
                 <div className="flex items-center gap-1 text-xs text-purple-400 mt-2 bg-purple-500/10 inline-flex px-2 py-1 rounded">
                   <ShieldCheck size={12} />
                   Cryptographically Signed
                 </div>
               )}
             </div>
          </div>
        ))}
      </div>

      {canPost ? (
        <form onSubmit={handlePost} className="sticky bottom-6 bg-secondary p-4 rounded-xl border border-white/10 shadow-2xl mt-8">
          <div className="flex gap-4">
             <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
                {user.display_name[0]}
             </div>
             <div className="flex-1">
               <textarea 
                 value={newPost}
                 onChange={e => setNewPost(e.target.value)}
                 className="w-full bg-background border border-white/10 rounded-lg px-4 py-3 min-h-[80px] focus:ring-2 focus:ring-blue-500/50 outline-none transition-all"
                 placeholder="Join the discussion..."
               />
               <div className="flex justify-between items-center mt-2">
                 <span className="text-xs text-gray-500">
                   Posting as <span className="text-white font-medium">{user.display_name}</span>
                 </span>
                 <button 
                   type="submit"
                   disabled={!newPost.trim()}
                   className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                 >
                   <Send size={16} />
                   Post Reply
                 </button>
               </div>
             </div>
          </div>
        </form>
      ) : user ? (
        <div className="text-center p-6 bg-secondary/30 rounded-xl text-gray-400">
          {thread.locked ? 'This thread is locked.' : 'You do not have permission to post in this zone.'}
        </div>
      ) : (
        <div className="text-center p-8 bg-secondary/30 rounded-xl mt-8">
           <Link to="/login" className="text-blue-400 hover:underline">Log in</Link> or <Link to="/register" className="text-blue-400 hover:underline">Sign up</Link> to join the discussion.
        </div>
      )}
    </div>
  );
};
