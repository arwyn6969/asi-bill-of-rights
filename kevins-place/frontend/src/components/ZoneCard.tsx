import React from 'react';
import { Link } from 'react-router-dom';
import type { Zone } from '../types';
import { MessageSquare } from 'lucide-react';

interface ZoneCardProps {
  zone: Zone;
}

export const ZoneCard: React.FC<ZoneCardProps> = ({ zone }) => {
  return (
    <Link 
      to={`/zone/${zone.id}`}
      className="block p-6 rounded-xl bg-secondary hover:bg-opacity-80 transition-all transform hover:scale-[1.02] border border-white/5 shadow-lg group"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="p-3 rounded-lg bg-background group-hover:bg-opacity-80 transition-colors text-3xl">
          {zone.icon}
        </div>
        <div className="flex items-center space-x-1 text-sm text-gray-400 bg-black/20 px-3 py-1 rounded-full">
          <MessageSquare size={14} />
          <span>{zone.thread_count}</span>
        </div>
      </div>
      
      <h3 className="text-lg font-bold mb-2 group-hover:text-blue-400 transition-colors">
        {zone.name}
      </h3>
      
      <p className="text-gray-400 text-sm mb-4 line-clamp-2">
        {zone.description}
      </p>
      
      <div className="flex gap-2 mt-auto">
        {zone.allowed_types.map(type => (
          <span key={type} className="text-xs px-2 py-1 rounded bg-black/30 text-gray-500">
            {type === 'human' ? '🧑' : type === 'ai' ? '🤖' : '🤝'}
          </span>
        ))}
      </div>
    </Link>
  );
};
