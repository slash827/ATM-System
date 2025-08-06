import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  text?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  className = '',
  text,
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  };

  const spinnerClasses = [
    'inline-block border-2 border-gray-300 border-t-primary-600 rounded-full animate-spin',
    sizeClasses[size],
    className,
  ].filter(Boolean).join(' ');

  if (text) {
    return (
      <div className="flex items-center justify-center gap-3">
        <div className={spinnerClasses} />
        <span className="text-gray-600 font-medium">{text}</span>
      </div>
    );
  }

  return <div className={spinnerClasses} />;
};

export default LoadingSpinner;
