import React from 'react';

interface ErrorMessageProps {
  message: string;
  details?: string;
  onRetry?: () => void;
  onDismiss?: () => void;
  className?: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  details,
  onRetry,
  onDismiss,
  className = '',
}) => {
  const classes = [
    'bg-error-50 border border-error-200 rounded-lg p-4',
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} role="alert">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg
            className="w-5 h-5 text-error-600"
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
        </div>
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-medium text-error-800">
            {message}
          </h3>
          {details && (
            <div className="mt-2 text-sm text-error-700">
              <p>{details}</p>
            </div>
          )}
          {(onRetry || onDismiss) && (
            <div className="mt-4 flex gap-3">
              {onRetry && (
                <button
                  type="button"
                  className="text-sm font-medium text-error-800 hover:text-error-900 underline"
                  onClick={onRetry}
                >
                  Try Again
                </button>
              )}
              {onDismiss && (
                <button
                  type="button"
                  className="text-sm font-medium text-error-700 hover:text-error-800"
                  onClick={onDismiss}
                >
                  Dismiss
                </button>
              )}
            </div>
          )}
        </div>
        {onDismiss && (
          <div className="ml-auto pl-3">
            <div className="-mx-1.5 -my-1.5">
              <button
                type="button"
                className="inline-flex rounded-md p-1.5 text-error-500 hover:bg-error-100 focus:outline-none focus:ring-2 focus:ring-error-600 focus:ring-offset-2 focus:ring-offset-error-50"
                onClick={onDismiss}
              >
                <span className="sr-only">Dismiss</span>
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;
