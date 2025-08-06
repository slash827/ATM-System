import React, { createContext, useContext, useReducer, useCallback } from 'react';
import type { AccountState, TransactionType } from '../types';

// ATM Context state
interface ATMState {
  account: AccountState;
  currentOperation: TransactionType | null;
  isConnected: boolean;
}

// ATM Context actions
type ATMAction =
  | { type: 'SET_ACCOUNT'; payload: string }
  | { type: 'SET_BALANCE'; payload: number }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_OPERATION'; payload: TransactionType | null }
  | { type: 'UPDATE_BALANCE'; payload: number }
  | { type: 'RESET_ACCOUNT' }
  | { type: 'SET_CONNECTION'; payload: boolean };

// Initial state
const initialState: ATMState = {
  account: {
    currentAccount: null,
    balance: null,
    isLoading: false,
    error: null,
    lastUpdated: null,
  },
  currentOperation: null,
  isConnected: true,
};

// Reducer function
function atmReducer(state: ATMState, action: ATMAction): ATMState {
  switch (action.type) {
    case 'SET_ACCOUNT':
      return {
        ...state,
        account: {
          ...state.account,
          currentAccount: action.payload,
          error: null,
        },
      };

    case 'SET_BALANCE':
      return {
        ...state,
        account: {
          ...state.account,
          balance: action.payload,
          lastUpdated: new Date(),
          error: null,
        },
      };

    case 'SET_LOADING':
      return {
        ...state,
        account: {
          ...state.account,
          isLoading: action.payload,
        },
      };

    case 'SET_ERROR':
      return {
        ...state,
        account: {
          ...state.account,
          error: action.payload,
          isLoading: false,
        },
      };

    case 'SET_OPERATION':
      return {
        ...state,
        currentOperation: action.payload,
      };

    case 'UPDATE_BALANCE':
      return {
        ...state,
        account: {
          ...state.account,
          balance: action.payload,
          lastUpdated: new Date(),
        },
      };

    case 'RESET_ACCOUNT':
      return {
        ...state,
        account: initialState.account,
        currentOperation: null,
      };

    case 'SET_CONNECTION':
      return {
        ...state,
        isConnected: action.payload,
      };

    default:
      return state;
  }
}

// Context interface
interface ATMContextType {
  state: ATMState;
  setAccount: (accountNumber: string) => void;
  setBalance: (balance: number) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setOperation: (operation: TransactionType | null) => void;
  updateBalance: (newBalance: number) => void;
  resetAccount: () => void;
  setConnection: (connected: boolean) => void;
}

// Create context
const ATMContext = createContext<ATMContextType | undefined>(undefined);

// ATM Provider component
export function ATMProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(atmReducer, initialState);

  const setAccount = useCallback((accountNumber: string) => {
    dispatch({ type: 'SET_ACCOUNT', payload: accountNumber });
  }, []);

  const setBalance = useCallback((balance: number) => {
    dispatch({ type: 'SET_BALANCE', payload: balance });
  }, []);

  const setLoading = useCallback((loading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  }, []);

  const setError = useCallback((error: string | null) => {
    dispatch({ type: 'SET_ERROR', payload: error });
  }, []);

  const setOperation = useCallback((operation: TransactionType | null) => {
    dispatch({ type: 'SET_OPERATION', payload: operation });
  }, []);

  const updateBalance = useCallback((newBalance: number) => {
    dispatch({ type: 'UPDATE_BALANCE', payload: newBalance });
  }, []);

  const resetAccount = useCallback(() => {
    dispatch({ type: 'RESET_ACCOUNT' });
  }, []);

  const setConnection = useCallback((connected: boolean) => {
    dispatch({ type: 'SET_CONNECTION', payload: connected });
  }, []);

  const value = {
    state,
    setAccount,
    setBalance,
    setLoading,
    setError,
    setOperation,
    updateBalance,
    resetAccount,
    setConnection,
  };

  return <ATMContext.Provider value={value}>{children}</ATMContext.Provider>;
}

// Custom hook to use ATM context
export function useATM() {
  const context = useContext(ATMContext);
  if (context === undefined) {
    throw new Error('useATM must be used within an ATMProvider');
  }
  return context;
}
