// Account related types
export interface Account {
  account_number: string;
  balance: number;
  created_at?: string;
  updated_at?: string;
  status?: AccountStatus;
}

export const AccountStatus = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  FROZEN: 'frozen'
} as const;

export type AccountStatus = typeof AccountStatus[keyof typeof AccountStatus];

// Account validation
export interface AccountValidation {
  isValid: boolean;
  errors: string[];
}

// Account number formatting
export interface AccountNumberFormat {
  raw: string;
  formatted: string;
  isComplete: boolean;
}

// Account state in the application
export interface AccountState {
  currentAccount: string | null;
  balance: number | null;
  isLoading: boolean;
  error: string | null;
  lastUpdated: Date | null;
}
