// Transfer-related// Time Deposit-related types
export interface CreateTimeDepositRequest {
  amount: number;
  duration_months: number;
  is_test_deposit?: boolean;
}
export interface TransferRequest {
  amount: number;
  recipient_account: string;
  message?: string;
}

export interface TransferResponse {
  success: boolean;
  message: string;
  sender_account: string;
  recipient_account: string;
  sender_previous_balance: number;
  sender_new_balance: number;
  transfer_amount: number;
  transfer_message?: string;
  timestamp: string;
}

// Time Deposit-related types
export interface CreateTimeDepositRequest {
  amount: number;
  duration_months: number;
}

export interface TimeDeposit {
  deposit_id: string;
  account_number: string;
  amount: number;
  duration_months: number;
  interest_rate: number;
  created_at: string;
  maturity_date: string;
  is_matured: boolean;
}

export interface TimeDepositResponse {
  success: boolean;
  message: string;
  deposit: TimeDeposit;
}

export interface ListTimeDepositsResponse {
  success: boolean;
  message: string;
  deposits: TimeDeposit[];
}

// Interest rate configuration for different durations
export interface InterestRateConfig {
  duration_months: number;
  interest_rate: number;
  description: string;
}

// Default interest rates (should match backend)
export const INTEREST_RATES: InterestRateConfig[] = [
  { duration_months: 3, interest_rate: 0.02, description: "3 months - 2% APY" },
  { duration_months: 6, interest_rate: 0.025, description: "6 months - 2.5% APY" },
  { duration_months: 12, interest_rate: 0.03, description: "12 months - 3% APY" },
  { duration_months: 18, interest_rate: 0.035, description: "18 months - 3.5% APY" },
  { duration_months: 24, interest_rate: 0.04, description: "24 months - 4% APY" },
  { duration_months: 36, interest_rate: 0.045, description: "36 months - 4.5% APY" },
  { duration_months: 48, interest_rate: 0.05, description: "48 months - 5% APY" },
  { duration_months: 60, interest_rate: 0.055, description: "60 months - 5.5% APY" }
];
