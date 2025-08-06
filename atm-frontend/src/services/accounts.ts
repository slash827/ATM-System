import apiClient from './api';
import type { 
  BalanceResponse, 
  TransactionRequest, 
  TransactionResponse, 
  HttpResponse 
} from '../types';

class AccountsService {
  /**
   * Get account balance
   * @param accountNumber - 6-digit account number
   * @returns Promise with balance response
   */
  async getBalance(accountNumber: string): Promise<HttpResponse<BalanceResponse>> {
    return apiClient.get<BalanceResponse>(`/accounts/${accountNumber}/balance`);
  }

  /**
   * Withdraw money from account
   * @param accountNumber - 6-digit account number
   * @param request - Transaction request with amount
   * @returns Promise with transaction response
   */
  async withdraw(
    accountNumber: string, 
    request: TransactionRequest
  ): Promise<HttpResponse<TransactionResponse>> {
    return apiClient.post<TransactionResponse>(
      `/accounts/${accountNumber}/withdraw`, 
      request
    );
  }

  /**
   * Deposit money to account
   * @param accountNumber - 6-digit account number
   * @param request - Transaction request with amount
   * @returns Promise with transaction response
   */
  async deposit(
    accountNumber: string, 
    request: TransactionRequest
  ): Promise<HttpResponse<TransactionResponse>> {
    return apiClient.post<TransactionResponse>(
      `/accounts/${accountNumber}/deposit`, 
      request
    );
  }

  /**
   * Validate account number format
   * @param accountNumber - Account number to validate
   * @returns Validation result
   */
  validateAccountNumber(accountNumber: string): { isValid: boolean; error?: string } {
    // Remove any spaces or special characters
    const cleaned = accountNumber.replace(/\D/g, '');
    
    if (cleaned.length === 0) {
      return { isValid: false, error: 'Account number is required' };
    }
    
    if (cleaned.length !== 6) {
      return { isValid: false, error: 'Account number must be exactly 6 digits' };
    }
    
    return { isValid: true };
  }

  /**
   * Format account number for display
   * @param accountNumber - Raw account number
   * @returns Formatted account number
   */
  formatAccountNumber(accountNumber: string): string {
    const cleaned = accountNumber.replace(/\D/g, '');
    return cleaned.slice(0, 6);
  }

  /**
   * Validate transaction amount
   * @param amount - Amount to validate
   * @returns Validation result
   */
  validateAmount(amount: string): { isValid: boolean; error?: string; numericValue?: number } {
    if (!amount || amount.trim() === '') {
      return { isValid: false, error: 'Amount is required' };
    }

    const numericValue = parseFloat(amount);
    
    if (isNaN(numericValue)) {
      return { isValid: false, error: 'Amount must be a valid number' };
    }
    
    if (numericValue <= 0) {
      return { isValid: false, error: 'Amount must be greater than zero' };
    }
    
    if (numericValue > 10000) {
      return { isValid: false, error: 'Amount cannot exceed $10,000' };
    }
    
    // Check for more than 2 decimal places
    if (amount.includes('.') && amount.split('.')[1]?.length > 2) {
      return { isValid: false, error: 'Amount cannot have more than 2 decimal places' };
    }
    
    return { isValid: true, numericValue };
  }

  /**
   * Format currency amount for display
   * @param amount - Numeric amount
   * @returns Formatted currency string
   */
  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(amount);
  }

  /**
   * Transfer money between accounts
   * @param senderAccount - 6-digit sender account number
   * @param request - Transfer request with amount, recipient, and message
   * @returns Promise with transfer response
   */
  async transferMoney(
    senderAccount: string,
    request: import('../types').TransferRequest
  ): Promise<import('../types').HttpResponse<import('../types').TransferResponse>> {
    return apiClient.post<import('../types').TransferResponse>(
      `/accounts/${senderAccount}/transfer`,
      request
    );
  }

  /**
   * Create a time deposit
   * @param accountNumber - 6-digit account number
   * @param request - Time deposit request with amount and duration
   * @returns Promise with time deposit response
   */
  async createTimeDeposit(
    accountNumber: string,
    request: import('../types').CreateTimeDepositRequest
  ): Promise<import('../types').HttpResponse<import('../types').TimeDepositResponse>> {
    return apiClient.post<import('../types').TimeDepositResponse>(
      `/accounts/${accountNumber}/time-deposits`,
      request
    );
  }

  /**
   * List time deposits for an account
   * @param accountNumber - 6-digit account number
   * @returns Promise with list of time deposits
   */
  async listTimeDeposits(
    accountNumber: string
  ): Promise<import('../types').HttpResponse<import('../types').ListTimeDepositsResponse>> {
    return apiClient.get<import('../types').ListTimeDepositsResponse>(
      `/accounts/${accountNumber}/time-deposits`
    );
  }

  /**
   * Mature a time deposit
   * @param depositId - Time deposit ID
   * @returns Promise with matured time deposit response
   */
  async matureTimeDeposit(
    depositId: string
  ): Promise<import('../types').HttpResponse<import('../types').TimeDepositResponse>> {
    return apiClient.post<import('../types').TimeDepositResponse>(
      `/time-deposits/${depositId}/mature`,
      {}
    );
  }

  /**
   * Calculate projected earnings for a time deposit
   * @param principal - Initial deposit amount
   * @param rate - Annual interest rate (as decimal, e.g., 0.05 for 5%)
   * @param months - Duration in months
   * @returns Projected final amount
   */
  calculateTimeDepositEarnings(principal: number, rate: number, months: number): number {
    // Simple interest calculation for time deposits
    const years = months / 12;
    const interest = principal * rate * years;
    return principal + interest;
  }

  /**
   * Format time deposit maturity date
   * @param createdAt - Creation date string
   * @param durationMonths - Duration in months
   * @returns Formatted maturity date
   */
  formatMaturityDate(createdAt: string, durationMonths: number): string {
    const created = new Date(createdAt);
    const maturity = new Date(created);
    maturity.setMonth(maturity.getMonth() + durationMonths);
    
    return maturity.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  /**
   * Check if a time deposit is close to maturity (within 30 days)
   * @param maturityDate - Maturity date string
   * @returns True if close to maturity
   */
  isCloseToMaturity(maturityDate: string): boolean {
    const maturity = new Date(maturityDate);
    const now = new Date();
    const thirtyDaysFromNow = new Date(now.getTime() + (30 * 24 * 60 * 60 * 1000));
    
    return maturity <= thirtyDaysFromNow && maturity > now;
  }
}

// Create and export the service instance
export const accountsService = new AccountsService();

// Export individual methods for easy importing
export const getBalance = accountsService.getBalance.bind(accountsService);
export const withdrawMoney = accountsService.withdraw.bind(accountsService);
export const depositMoney = accountsService.deposit.bind(accountsService);
export const transferMoney = accountsService.transferMoney.bind(accountsService);
export const createTimeDeposit = accountsService.createTimeDeposit.bind(accountsService);
export const listTimeDeposits = accountsService.listTimeDeposits.bind(accountsService);
export const matureTimeDeposit = accountsService.matureTimeDeposit.bind(accountsService);
export default accountsService;
