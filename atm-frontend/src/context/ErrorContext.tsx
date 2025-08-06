import React, { createContext, useContext, useReducer, useCallback } from 'react';
import type { ErrorState, AppError, ErrorType } from '../types';

// Error Context actions
type ErrorAction =
  | { type: 'SET_ERROR'; payload: AppError }
  | { type: 'CLEAR_ERROR' }
  | { type: 'CLEAR_ALL_ERRORS' }
  | { type: 'ADD_ERROR'; payload: AppError };

// Initial state
const initialState: ErrorState = {
  hasError: false,
  error: null,
  errors: [],
};

// Reducer function
function errorReducer(state: ErrorState, action: ErrorAction): ErrorState {
  switch (action.type) {
    case 'SET_ERROR':
      return {
        hasError: true,
        error: action.payload,
        errors: [action.payload, ...state.errors.slice(0, 4)], // Keep last 5 errors
      };

    case 'CLEAR_ERROR':
      return {
        hasError: false,
        error: null,
        errors: state.errors,
      };

    case 'ADD_ERROR':
      return {
        ...state,
        errors: [action.payload, ...state.errors.slice(0, 4)],
      };

    case 'CLEAR_ALL_ERRORS':
      return initialState;

    default:
      return state;
  }
}

// Context interface
interface ErrorContextType {
  state: ErrorState;
  setError: (message: string, type?: ErrorType, details?: string) => void;
  clearError: () => void;
  clearAllErrors: () => void;
  addError: (message: string, type?: ErrorType, details?: string) => void;
}

// Create context
const ErrorContext = createContext<ErrorContextType | undefined>(undefined);

// Error Provider component
export function ErrorProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(errorReducer, initialState);

  const createError = useCallback((
    message: string, 
    type: ErrorType = 'unknown', 
    details?: string
  ): AppError => ({
    code: type.toUpperCase(),
    message,
    details,
    timestamp: new Date(),
  }), []);

  const setError = useCallback((
    message: string, 
    type: ErrorType = 'unknown', 
    details?: string
  ) => {
    const error = createError(message, type, details);
    dispatch({ type: 'SET_ERROR', payload: error });
  }, [createError]);

  const clearError = useCallback(() => {
    dispatch({ type: 'CLEAR_ERROR' });
  }, []);

  const clearAllErrors = useCallback(() => {
    dispatch({ type: 'CLEAR_ALL_ERRORS' });
  }, []);

  const addError = useCallback((
    message: string, 
    type: ErrorType = 'unknown', 
    details?: string
  ) => {
    const error = createError(message, type, details);
    dispatch({ type: 'ADD_ERROR', payload: error });
  }, [createError]);

  const value = {
    state,
    setError,
    clearError,
    clearAllErrors,
    addError,
  };

  return <ErrorContext.Provider value={value}>{children}</ErrorContext.Provider>;
}

// Custom hook to use Error context
export function useError() {
  const context = useContext(ErrorContext);
  if (context === undefined) {
    throw new Error('useError must be used within an ErrorProvider');
  }
  return context;
}
