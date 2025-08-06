import React from 'react';
import type { CardProps } from '../../types';

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  title,
  description,
}) => {
  const classes = [
    'bg-white rounded-lg shadow-lg border border-gray-200 p-4',
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className={classes}>
      {(title || description) && (
        <div className="mb-4">
          {title && (
            <h2 className="text-lg font-bold text-gray-900 mb-1">
              {title}
            </h2>
          )}
          {description && (
            <p className="text-gray-600 text-sm">
              {description}
            </p>
          )}
        </div>
      )}
      {children}
    </div>
  );
};

export default Card;
