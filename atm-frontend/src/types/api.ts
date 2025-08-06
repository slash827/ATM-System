// API Response interfaces matching the backend
export interface ApiResponse<T = any> {
  success?: boolean;
  message?: string;
  data?: T;
}

// Balance Response
export interface BalanceResponse {
  balance: number;
}

// Transaction Request
export interface TransactionRequest {
  amount: number;
  pin?: string; // Optional for future PIN validation
}

// Transaction Response
export interface TransactionResponse {
  success: boolean;
  message: string;
  new_balance: number;
  transaction_id?: string;
}

// Health Check Response
export interface HealthResponse {
  status: string;
  timestamp: string;
  environment: string;
  debug: boolean;
}

// API Error Response
export interface ApiError {
  detail: string;
  error_code?: string;
  requested_amount?: number;
  current_balance?: number;
  timestamp?: string;
}

// HTTP Response wrapper
export interface HttpResponse<T = any> {
  data: T;
  status: number;
  statusText: string;
}

// API Client configuration
export interface ApiClientConfig {
  baseURL: string;
  timeout?: number;
  headers?: Record<string, string>;
}
