import React from 'react';

interface BadgeProps {
  type: 'human' | 'ai' | 'hybrid';
  className?: string; // Allow custom styling
}

export const Badge: React.FC<BadgeProps> = ({ type, className: extraClass = '' }) => {
  const config = {
    human: { emoji: '🧑', label: 'Human', className: 'badge-human' },
    ai: { emoji: '🤖', label: 'AI', className: 'badge-ai' },
    hybrid: { emoji: '🔀', label: 'Hybrid', className: 'badge-human' },
  };

  const { emoji, label, className } = config[type] || config.human;

  return (
    <span className={`badge ${className} ${extraClass}`}>
      {emoji} {label}
    </span>
  );
};
