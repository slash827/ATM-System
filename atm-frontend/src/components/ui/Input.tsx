import React from 'react';
import type { InputProps } from '../../types';

const Input: React.FC<InputProps> = ({
  value,
  onChange,
  placeholder,
  type = 'text',
  maxLength,
  disabled = false,
  error,
  className = '',
  autoFocus = false,
}) => {
  const baseClasses = 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-base text-center font-mono transition-colors duration-200';
  const errorClasses = error ? 'border-error-500 focus:ring-error-500 focus:border-error-500' : '';
  
  const classes = [
    baseClasses,
    errorClasses,
    className,
  ].filter(Boolean).join(' ');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  return (
    <div className="w-full">
      <input
        type={type}
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        maxLength={maxLength}
        disabled={disabled}
        className={classes}
        autoFocus={autoFocus}
        aria-invalid={!!error}
        aria-describedby={error ? 'input-error' : undefined}
      />
      {error && (
        <div id="input-error" className="text-error-600 text-sm font-medium mt-2 flex items-center">
          <svg
            className="w-4 h-4 mr-1"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
          {error}
        </div>
      )}
    </div>
  );
};

export default Input;
