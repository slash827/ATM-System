import React, { createContext, useContext, useReducer, useCallback } from 'react';
import type { LoadingState } from '../types';

// Loading Context state
interface LoadingContextState {
  global: LoadingState;
  operations: Record<string, LoadingState>;
}

// Loading Context actions
type LoadingAction =
  | { type: 'SET_GLOBAL_LOADING'; payload: Partial<LoadingState> }
  | { type: 'SET_OPERATION_LOADING'; payload: { operation: string; state: Partial<LoadingState> } }
  | { type: 'CLEAR_OPERATION_LOADING'; payload: string }
  | { type: 'CLEAR_ALL_LOADING' };

// Initial state
const initialState: LoadingContextState = {
  global: {
    isLoading: false,
    operation: undefined,
    progress: undefined,
  },
  operations: {},
};

// Reducer function
function loadingReducer(state: LoadingContextState, action: LoadingAction): LoadingContextState {
  switch (action.type) {
    case 'SET_GLOBAL_LOADING':
      return {
        ...state,
        global: {
          ...state.global,
          ...action.payload,
        },
      };

    case 'SET_OPERATION_LOADING':
      return {
        ...state,
        operations: {
          ...state.operations,
          [action.payload.operation]: {
            ...state.operations[action.payload.operation],
            ...action.payload.state,
          },
        },
      };

    case 'CLEAR_OPERATION_LOADING':
      const { [action.payload]: removed, ...remainingOperations } = state.operations;
      return {
        ...state,
        operations: remainingOperations,
      };

    case 'CLEAR_ALL_LOADING':
      return initialState;

    default:
      return state;
  }
}

// Context interface
interface LoadingContextType {
  state: LoadingContextState;
  setGlobalLoading: (loading: boolean, operation?: string, progress?: number) => void;
  setOperationLoading: (operation: string, loading: boolean, progress?: number) => void;
  clearOperationLoading: (operation: string) => void;
  clearAllLoading: () => void;
  isLoading: (operation?: string) => boolean;
  getProgress: (operation?: string) => number | undefined;
}

// Create context
const LoadingContext = createContext<LoadingContextType | undefined>(undefined);

// Loading Provider component
export function LoadingProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(loadingReducer, initialState);

  const setGlobalLoading = useCallback((
    loading: boolean, 
    operation?: string, 
    progress?: number
  ) => {
    dispatch({
      type: 'SET_GLOBAL_LOADING',
      payload: { isLoading: loading, operation, progress },
    });
  }, []);

  const setOperationLoading = useCallback((
    operation: string, 
    loading: boolean, 
    progress?: number
  ) => {
    dispatch({
      type: 'SET_OPERATION_LOADING',
      payload: {
        operation,
        state: { isLoading: loading, operation, progress },
      },
    });
  }, []);

  const clearOperationLoading = useCallback((operation: string) => {
    dispatch({ type: 'CLEAR_OPERATION_LOADING', payload: operation });
  }, []);

  const clearAllLoading = useCallback(() => {
    dispatch({ type: 'CLEAR_ALL_LOADING' });
  }, []);

  const isLoading = useCallback((operation?: string) => {
    if (operation) {
      return state.operations[operation]?.isLoading || false;
    }
    return state.global.isLoading || Object.values(state.operations).some(op => op.isLoading);
  }, [state]);

  const getProgress = useCallback((operation?: string) => {
    if (operation) {
      return state.operations[operation]?.progress;
    }
    return state.global.progress;
  }, [state]);

  const value = {
    state,
    setGlobalLoading,
    setOperationLoading,
    clearOperationLoading,
    clearAllLoading,
    isLoading,
    getProgress,
  };

  return <LoadingContext.Provider value={value}>{children}</LoadingContext.Provider>;
}

// Custom hook to use Loading context
export function useLoading() {
  const context = useContext(LoadingContext);
  if (context === undefined) {
    throw new Error('useLoading must be used within a LoadingProvider');
  }
  return context;
}
