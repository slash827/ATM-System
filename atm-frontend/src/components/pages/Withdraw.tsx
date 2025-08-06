import React, { useState } from 'react';
import { Card, Button, Input } from '../ui';
import { accountsService } from '../../services/accounts';
import { useError, useLoading } from '../../context';

interface WithdrawProps {
  accountNumber: string;
  onBack: () => void;
}

const Withdraw: React.FC<WithdrawProps> = ({ accountNumber, onBack }) => {
  const [amount, setAmount] = useState('');
  const [result, setResult] = useState<{
    success: boolean;
    message: string;
    newBalance?: number;
  } | null>(null);
  const [amountError, setAmountError] = useState('');
  const { setError } = useError();
  const { setGlobalLoading } = useLoading();

  const handleAmountChange = (value: string) => {
    setAmount(value);
    setAmountError('');
    setResult(null);
  };

  const handleWithdraw = async () => {
    // Validate amount
    const validation = accountsService.validateAmount(amount);
    if (!validation.isValid) {
      setAmountError(validation.error || 'Invalid amount');
      return;
    }

    try {
      setGlobalLoading(true, 'Processing withdrawal...');
      const response = await accountsService.withdraw(accountNumber, {
        amount: validation.numericValue!
      });
      
      setResult({
        success: true,
        message: response.data.message,
        newBalance: response.data.new_balance
      });
      setAmount('');
    } catch (error: any) {
      setResult({
        success: false,
        message: error.detail || 'Failed to withdraw money'
      });
    } finally {
      setGlobalLoading(false);
    }
  };

  const handleNewTransaction = () => {
    setResult(null);
    setAmount('');
    setAmountError('');
  };

  return (
    <div className="space-y-6">
      <Card
        title="Cash Withdrawal"
        description={`Withdraw money from account ${accountNumber}`}
      >
        {!result ? (
          <div className="space-y-4">
            <div>
              <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
                Amount to Withdraw
              </label>
              <Input
                value={amount}
                onChange={handleAmountChange}
                placeholder="Enter amount (e.g., 100.00)"
                type="text"
                error={amountError}
                autoFocus
              />
              <p className="text-xs text-gray-500 mt-1">
                Maximum withdrawal: $10,000
              </p>
            </div>
            
            <div className="flex justify-center gap-3">
              <Button 
                variant="secondary" 
                onClick={onBack}
              >
                Cancel
              </Button>
              <Button 
                variant="primary" 
                onClick={handleWithdraw}
                disabled={!amount.trim()}
              >
                Withdraw Money
              </Button>
            </div>
          </div>
        ) : (
          <div className="text-center space-y-6">
            <div className={`border rounded-lg p-6 ${
              result.success 
                ? 'bg-success-50 border-success-200' 
                : 'bg-error-50 border-error-200'
            }`}>
              <div className={`text-lg font-semibold mb-2 ${
                result.success ? 'text-success-800' : 'text-error-800'
              }`}>
                {result.success ? '✅ Withdrawal Successful' : '❌ Withdrawal Failed'}
              </div>
              <p className={`${
                result.success ? 'text-success-700' : 'text-error-700'
              }`}>
                {result.message}
              </p>
              {result.success && result.newBalance !== undefined && (
                <div className="mt-4 pt-4 border-t border-success-200">
                  <p className="text-sm text-success-600">New Balance:</p>
                  <div className="text-2xl font-bold text-success-700 font-mono">
                    {accountsService.formatCurrency(result.newBalance)}
                  </div>
                </div>
              )}
            </div>
            
            <div className="flex justify-center gap-3">
              <Button 
                variant="outline" 
                onClick={handleNewTransaction}
              >
                New Withdrawal
              </Button>
              <Button 
                variant="secondary" 
                onClick={onBack}
              >
                Back to Operations
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};

export default Withdraw;
