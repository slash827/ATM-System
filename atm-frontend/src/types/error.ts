// Error types for the application
export interface AppError {
  code: string;
  message: string;
  details?: string;
  timestamp: Date;
  context?: Record<string, any>;
}

// Error categories
export type ErrorType = 
  | 'network'
  | 'validation'
  | 'account_not_found'
  | 'insufficient_funds'
  | 'invalid_amount'
  | 'server_error'
  | 'unknown';

// Error state for context
export interface ErrorState {
  hasError: boolean;
  error: AppError | null;
  errors: AppError[];
}

// Form validation errors
export interface FormErrors {
  [field: string]: string | undefined;
}

// API Error mapping
export interface ApiErrorMapping {
  status: number;
  type: ErrorType;
  message: string;
}

// Error boundary props
export interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: any;
}
