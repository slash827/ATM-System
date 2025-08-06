// Transaction types
export interface Transaction {
  id?: string;
  account_number: string;
  transaction_type: TransactionType;
  amount: number;
  balance_before?: number;
  balance_after?: number;
  timestamp: Date;
  status: TransactionStatus;
}

export type TransactionType = 'deposit' | 'withdrawal' | 'balance_inquiry';

export type TransactionStatus = 'pending' | 'completed' | 'failed' | 'cancelled';

// Transaction form data
export interface TransactionFormData {
  account_number: string;
  amount: string;
  operation: TransactionType;
}

// Transaction validation
export interface TransactionValidation {
  isValid: boolean;
  errors: {
    account_number?: string;
    amount?: string;
    general?: string;
  };
}

// Transaction history (for local state)
export interface TransactionHistory {
  transactions: Transaction[];
  totalCount: number;
  lastUpdated: Date;
}

// Amount formatting
export interface AmountFormat {
  raw: string;
  formatted: string;
  numeric: number;
  isValid: boolean;
}
