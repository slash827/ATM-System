// Test utilities without dependencies - can be updated when testing libraries are installed
// This provides the structure for comprehensive testing

// Mock data for testing
export const mockAccountData = {
  validAccount: '123456',
  invalidAccount: '999999',
  shortAccount: '123',
  longAccount: '1234567',
  nonNumericAccount: 'abc123',
}

export const mockTransactionData = {
  successfulWithdraw: {
    account_number: '123456',
    amount: 100,
    new_balance: 900,
    transaction_id: 'txn_123'
  },
  insufficientFunds: {
    account_number: '123456',
    amount: 2000,
    error: 'Insufficient funds'
  },
}

export const mockAPIResponses = {
  getBalance: {
    success: {
      account_number: '123456',
      balance: 1000.00,
      status: 'active'
    },
    error: {
      detail: 'Account not found'
    }
  }
}

// Test constants
export const TEST_CONSTANTS = {
  DEMO_ACCOUNTS: ['123456', '654321', '111111'],
  MAX_ACCOUNT_LENGTH: 6,
  MIN_WITHDRAWAL: 10,
  MAX_WITHDRAWAL: 1000,
}
