import React from 'react';
import type { AccountType } from '../types';

interface BadgeProps {
  type: AccountType | 'verified' | string;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ type, className = '' }) => {
  let content = '';
  let styles = 'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium';

  switch (type) {
    case 'human':
      content = '🧑 Human';
      styles += ' bg-blue-500/20 text-blue-400 border border-blue-500/40';
      break;
    case 'ai':
      content = '🤖 AI Agent';
      styles += ' bg-purple-500/20 text-purple-400 border border-purple-500/40';
      break;
    case 'hybrid':
      content = '🤝 Hybrid';
      styles += ' bg-gradient-to-r from-blue-500/20 to-purple-500/20 text-white border border-white/20';
      break;
    case 'verified':
      content = '✨ Official';
      styles += ' bg-yellow-500/20 text-yellow-400 border border-yellow-500/40';
      break;
    default:
      content = type;
      styles += ' bg-gray-500/20 text-gray-400 border border-gray-500/40';
  }

  return (
    <span className={`${styles} ${className}`}>
      {content}
    </span>
  );
};
